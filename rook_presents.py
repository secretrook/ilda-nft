from src.ILDA import *
from src.projector import *

alice = ILDA_FILE('data/alice.ild')

projector1 = Projector()
projector1.dissociate(alice.data_records)