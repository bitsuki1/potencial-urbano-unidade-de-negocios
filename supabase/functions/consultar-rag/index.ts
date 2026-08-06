// consultar-rag — cérebro do Assistente (Gen RAG). Embeda a pergunta (Gemini
// gemini-embedding-001, 768d p/ casar o corpus) e chama public.consultar_corpus
// -> devolve os trechos COM CITAÇÃO (1.7) e, por cima deles, uma RESPOSTA EM PROSA
// (Gemini Flash) que só redige sobre os trechos — nunca inventa dispositivo nem
// calcula valor (1.3: número nasce em engine). Sem resultado, avisa NÃO-FUNDAMENTADA.
// A prosa é camada de redação: se a síntese falhar, os trechos seguem sendo a resposta.
// Requer secret: GEMINI_API_KEY. SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY são
// injetados pelo runtime. Deployada no projeto potencial-urbano-iptu-tdc (verify_jwt on).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const MODELO_SINTESE = "gemini-2.5-flash";

const INSTRUCAO_SINTESE = `Você é o assistente jurídico do Potencial Urbano (IPTU/TDC do Município de São Paulo).
Responda à pergunta do usuário em português do Brasil, em prosa clara e direta, usando EXCLUSIVAMENTE os trechos normativos fornecidos.
Regras invioláveis:
1. TODA afirmação deve citar o dispositivo que a sustenta, entre parênteses, no formato (Lei nº 16.050/2014, art. 128) ou (Decreto nº 57.776/2017, art. 3º) — use exatamente as leis/artigos dos trechos fornecidos.
2. NUNCA invente número de lei, artigo, prazo ou valor que não esteja literalmente nos trechos.
3. NUNCA calcule valores monetários nem estime preços — se a pergunta pedir cálculo, diga que o valor é apurado pelo engine determinístico da plataforma (tela Carteira) e explique apenas a regra legal.
4. Se os trechos não bastarem para responder, diga explicitamente o que falta — não complete com conhecimento externo.
5. Seja conciso: 1 a 4 parágrafos.`;

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const { pergunta, dominio = null, k = 8, sintetizar = true } = await req.json();
    if (!pergunta || typeof pergunta !== "string") {
      return json({ erro: "Envie { pergunta: string, dominio?, k?, sintetizar? }" }, 400);
    }
    const gkey = Deno.env.get("GEMINI_API_KEY");
    if (!gkey) return json({ erro: "GEMINI_API_KEY nao configurada (secret do Supabase)." }, 500);

    // 1) embedding da pergunta (768d; RETRIEVAL_QUERY casa com o corpus embedado
    //    como RETRIEVAL_DOCUMENT — sem o taskType a similaridade degrada)
    const er = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${gkey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "models/gemini-embedding-001",
          content: { parts: [{ text: pergunta }] },
          taskType: "RETRIEVAL_QUERY",
          outputDimensionality: 768,
        }),
      },
    );
    if (!er.ok) return json({ erro: `Falha no embedding Gemini: ${er.status} ${await er.text()}` }, 502);
    const ej = await er.json();
    const emb: number[] = ej?.embedding?.values;
    if (!emb || emb.length !== 768) return json({ erro: "Embedding invalido (esperado 768d)." }, 502);

    // 2) busca (filtro dominio + citavel + vigencia + cosseno) via wrapper publico
    const sb = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const { data, error } = await sb.rpc("consultar_corpus", { emb, dominio_f: dominio, k });
    if (error) return json({ erro: `Falha na busca: ${error.message}` }, 500);

    if (!data || data.length === 0) {
      return json({
        pergunta,
        fundamentada: false,
        aviso: "NAO-FUNDAMENTADA: nenhum dispositivo recuperado. (O corpus pode nao estar carregado ainda, ou a pergunta esta fora do escopo IPTU/TDC-SP.)",
        resultados: [],
      });
    }

    // 3) síntese em prosa POR CIMA dos trechos (opcional; falha nunca derruba a consulta)
    let resposta: string | null = null;
    if (sintetizar) {
      try {
        const contexto = data
          .map((r: Record<string, unknown>, i: number) => {
            const cit = typeof r.citacao === "object" ? JSON.stringify(r.citacao) : String(r.citacao ?? "");
            return `[Trecho ${i + 1}] lei=${r.lei_id} citacao=${cit}\n${r.texto}`;
          })
          .join("\n\n");
        const sr = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/${MODELO_SINTESE}:generateContent?key=${gkey}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              systemInstruction: { parts: [{ text: INSTRUCAO_SINTESE }] },
              contents: [{ role: "user", parts: [{ text: `Pergunta: ${pergunta}\n\nTrechos normativos:\n\n${contexto}` }] }],
              generationConfig: { temperature: 0.2, maxOutputTokens: 1024 },
            }),
          },
        );
        if (sr.ok) {
          const sj = await sr.json();
          const t = sj?.candidates?.[0]?.content?.parts?.map((p: { text?: string }) => p.text ?? "").join("");
          if (t && t.trim().length > 0) resposta = t.trim();
        }
      } catch (_e) {
        // síntese é camada opcional — a resposta fundamentada são os trechos
      }
    }

    return json({ pergunta, fundamentada: true, resposta, resultados: data });
  } catch (e) {
    return json({ erro: String(e) }, 500);
  }
});

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}
