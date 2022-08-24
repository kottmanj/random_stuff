import tequila as tq

geom = "H 0.0 0.0 0.0\nH 0.0 0.0 {}"

steps=50
start=0.5
step=0.1
data={"mp2":{}, "fci":{}, "ref":{}}
for x in range(steps):
    R = start + x*step
    mol = tq.Molecule(geometry=geom.format(R))
    mp2 = mol.compute_energy("mp2")
    fci = mol.compute_energy("fci")
    ref = tq.Molecule(geometry=geom.format(R), basis_set="aug-cc-pVQZ").compute_energy("fci")
    data["mp2"][R] = [mp2]
    data["fci"][R] = [fci]
    data["ref"][R] = [ref]

with open("data.out", "w") as f:
    f.write(str(data))
