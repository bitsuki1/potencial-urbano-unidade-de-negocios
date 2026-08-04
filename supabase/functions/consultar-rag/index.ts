// consultar-rag — cérebro do Assistente (Gen RAG). Embeda a pergunta (Gemini
// gemini-embedding-001, 768d p/ casar o corpus) e chama public.consultar_corpus
// -> devolve os trechos COM CITAÇÃO (1.7). Nunca inventa: sem resultado, avisa.
// Requer secret: GEMINI_API_KEY. SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY são
// injetados pelo runtime. Deployada no projeto potencial-urbano-iptu-tdc (verify_jwt on).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const { pergunta, dominio = null, k = 8 } = await req.json();
    if (!pergunta || typeof pergunta !== "string") {
      return json({ erro: "Envie { pergunta: string, dominio?, k? }" }, 400);
    }
    const gkey = Deno.env.get("GEMINI_API_KEY");
    if (!gkey) return json({ erro: "GEMINI_API_KEY nao configurada (secret do Supabase)." }, 500);

    // 1) embedding da pergunta (768d, p/ casar o corpus gemini-embedding-001)
    const er = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${gkey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "models/gemini-embedding-001",
          content: { parts: [{ text: pergunta }] },
          outputDimensionality: 768,
        }),
      },
    );
    if (!er.ok) return json({ erro: `Falha no embedding Gemini: ${er.status} ${await er.text()}` }, 502);
    const ej = await er.json();
    const emb: number[] = ej?.embedding?.values;
    if (!emb || emb.length !== 768) return json({ erro: "Embedding invalido (esperado 768d)." }, 502);

    // 2) busca hibrida (filtro dominio + cosseno) via wrapper publico
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
    return json({ pergunta, fundamentada: true, resultados: data });
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
