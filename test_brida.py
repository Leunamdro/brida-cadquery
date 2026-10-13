""" Ejecutar con:  pytest -v test_brida.py
"""
import math

import pytest

from brida import (D_AGUJ, D_EXT, D_INT, ESPESOR, N_AGUJ, PCD, CHAMFER,
                   construir_brida)

TOL = 0.01  # mm / mm3


@pytest.fixture(scope="module")
def solido():
    return construir_brida().val()


def test_es_un_solo_solido_valido(solido):
    assert solido.isValid()
    assert len(solido.Solids()) == 1


def test_volumen_contra_calculo_manual(solido):
    area = math.pi / 4 * (D_EXT**2 - D_INT**2 - N_AGUJ * D_AGUJ**2)
    assert solido.Volume() == pytest.approx(area * ESPESOR - 2* math.pi * (D_EXT/2 - CHAMFER/3) * 1/2 * CHAMFER * CHAMFER, abs=TOL)


def test_caja_envolvente(solido):
    bb = solido.BoundingBox()
    assert bb.xlen == pytest.approx(D_EXT, abs=TOL)
    assert bb.ylen == pytest.approx(D_EXT, abs=TOL)
    assert bb.zlen == pytest.approx(ESPESOR, abs=TOL)


def test_numero_de_agujeros(solido):
    # caras cilíndricas = contorno exterior + agujero central + n agujeros
    cilindros = [f for f in solido.Faces() if f.geomType() == "CYLINDER"]
    assert len(cilindros) == 2 + N_AGUJ


def test_agujeros_sobre_el_pcd(solido):
    # cada agujero deja 2 aristas circulares (cara superior e inferior)
    radios = [
        math.hypot(e.Center().x, e.Center().y)
        for e in solido.Edges()
        if e.geomType() == "CIRCLE"
        and e.radius() == pytest.approx(D_AGUJ / 2, abs=TOL)
    ]
    assert len(radios) == 2 * N_AGUJ
    for r in radios:
        assert r == pytest.approx(PCD / 2, abs=TOL)
