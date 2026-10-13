"""Ejercicio 1 de CadQuery: brida circular paramétrica.

Cada parámetro equivale a una celda de la hoja de cálculo de FreeCAD.
Cambia un valor, ejecuta el script y se regenera el sólido.
"""
import cadquery as cq

# Parámetros (mm)
D_EXT = 130.0   # diámetro exterior
D_INT = 50.0    # diámetro del agujero central
ESPESOR = 13.0  # espesor de la brida
PCD = 90.0      # diámetro del círculo de agujeros
D_AGUJ = 11.0   # diámetro de los agujeros de tornillo (M10, paso medio)
N_AGUJ = 6      # número de agujeros
CHAMFER = 3     # cateto de chaflan a 45º

def construir_brida(d_ext=D_EXT, d_int=D_INT, espesor=ESPESOR,
                    pcd=PCD, d_aguj=D_AGUJ, n_aguj=N_AGUJ, chamfer=CHAMFER):
    """Devuelve el sólido. Equivale a un croquis en XY + pad + taladros."""
    return (
        cq.Workplane("XY")                						 # plano de croquis XY, Z = 0
        .circle(d_ext / 2)                						 # contorno exterior
        .circle(d_int / 2)                						 # agujero central (perfil interior)
        .extrude(espesor)                 						 # pad en +Z
        .faces(">Z").workplane()          						 # nuevo plano sobre la cara superior
        .polarArray(pcd / 2, 0, 360, n_aguj)  						 # n agujeros sobre el PCD
        .hole(d_aguj)                      						 # pasantes
        .faces(">Z").edges("not %LINE").edges(cq.selectors.RadiusNthSelector(-1)) 	 # filos
        .chamfer(CHAMFER)								 # chaflan
)


if __name__ == "__main__":
    brida = construir_brida()
    cq.exporters.export(brida, "brida.step")
    print(f"Volumen: {brida.val().Volume():.2f} mm3")
    print("Exportado: brida.step")
