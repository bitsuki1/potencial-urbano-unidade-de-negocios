#!/usr/bin/env python3
"""vedacao_geo.py — Vedação geométrica Art. 124 §2º (Lei 16.050/2014).

Carrega o shapefile ZEPEC_AUE (741 polígonos, EPSG:31983 — SIRGAS 2000 UTM 23S) e
fornece consulta ponto-em-AUE para lotes com coordenadas conhecidas.

Art. 124 §2º: "É vedada a transferência de potencial construtivo oriundo de imóveis
situados em Áreas de Urbanização Especial (AUE) e Áreas de Proteção Paisagística (APPa)."

Uso no pipeline:
    from vedacao_geo import VedacaoGeo
    vg = VedacaoGeo()                         # carrega shapefile; sem arquivo → skip silencioso
    if vg.disponivel:
        vedado = vg.em_aue(x_utm, y_utm)      # True se ponto cai em polígono AUE

Coordenadas em UTM (EPSG:31983) — mesma projeção dos shapefiles ZEPEC/LOTES.
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SHP_DEFAULT = REPO / "zepec" / "shapefiles" / "ZEPEC_AUE.shp"


class VedacaoGeo:
    def __init__(self, shp_path=None):
        self.disponivel = False
        self._prepared = []
        self._tree = None
        p = Path(shp_path) if shp_path else SHP_DEFAULT
        if not p.exists():
            return
        try:
            import shapefile
            from shapely.geometry import shape as shp_shape
            from shapely.ops import unary_union
            from shapely.strtree import STRtree
            from shapely.prepared import prep

            r = shapefile.Reader(str(p))
            polys = []
            for i in range(len(r)):
                try:
                    g = shp_shape(r.shape(i).__geo_interface__)
                    if not g.is_valid:
                        g = g.buffer(0)
                    if not g.is_empty:
                        polys.append(g)
                except Exception:
                    pass
            if not polys:
                return
            aue = unary_union(polys)
            self._prepared = [prep(aue)]
            self._tree = STRtree([aue])
            self.disponivel = True
            self.n_poligonos = len(polys)
        except ImportError:
            pass

    def em_aue(self, x_utm, y_utm):
        """Retorna True se o ponto (UTM 23S) está dentro de algum polígono AUE."""
        if not self.disponivel:
            return False
        from shapely.geometry import Point
        pt = Point(x_utm, y_utm)
        for idx in self._tree.query(pt):
            if self._prepared[int(idx)].contains(pt):
                return True
        return False

    def lotes_em_aue(self, lotes_coords):
        """Recebe dict {sql_mestre: (x_utm, y_utm)} e retorna set dos SQL vedados."""
        if not self.disponivel:
            return set()
        vedados = set()
        for sql, (x, y) in lotes_coords.items():
            if self.em_aue(x, y):
                vedados.add(sql)
        return vedados


if __name__ == "__main__":
    vg = VedacaoGeo()
    if vg.disponivel:
        print(f"vedacao_geo: shapefile AUE carregado ({vg.n_poligonos} polígonos)")
        print("  Pronto para consulta ponto-em-AUE (EPSG:31983).")
        print("  Uso: vg.em_aue(x_utm, y_utm) → True/False")
    else:
        print("vedacao_geo: shapefile AUE NÃO encontrado ou dependências ausentes.")
        print(f"  Esperado em: {SHP_DEFAULT}")
