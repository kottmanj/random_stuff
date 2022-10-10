import tequila as tq

mol = tq.Molecule(geometry="be 0.0 0.0 0.0\n H 0.0 0.0 1.0\nH 0.0 0.0 -1.0", basis_set="sto-3g")

U = mol.make_ansatz(name="SPA", edges=[(0,1,2),(3,4,5)])
U.export_to(filename="spa_beh2.pdf")
U.export_to(filename="spa_beh2.png")
