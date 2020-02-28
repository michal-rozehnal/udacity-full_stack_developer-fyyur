from enum import Enum, auto

class EnumBase(Enum):

  @classmethod
  def choices(cls):
    return [(choice, choice.name) for choice in cls]

  @classmethod
  def coerce(cls, item):
    return cls(int(item)) if not isinstance(item, cls) else item

  def __str__(self):
    return str(self.value)

class GenresEnum(EnumBase):
  Alternative = auto()
  Blues = auto()
  Classical = auto()
  Country = auto()
  Electronic = auto()
  Folk = auto()
  Funk = auto()
  Hip_Hop = auto()
  Heavy_Metal = auto()
  Instrumental = auto()
  Jazz = auto()
  Musical_Theatre = auto()
  Pop = auto()
  Punk = auto()
  R_n_B = auto()
  Reggae = auto()
  Rock_n_Roll = auto()
  Soul = auto()
  Other = auto()

class StateEnum(EnumBase):
  AL = auto()
  AK = auto()
  AZ = auto()
  AR = auto()
  CA = auto()
  CO = auto()
  CT = auto()
  DE = auto()
  DC = auto()
  FL = auto()
  GA = auto()
  HI = auto()
  ID = auto()
  IL = auto()
  IN = auto()
  IA = auto()
  KS = auto()
  KY = auto()
  LA = auto()
  ME = auto()
  MT = auto()
  NE = auto()
  NV = auto()
  NH = auto()
  NJ = auto()
  NM = auto()
  NY = auto()
  NC = auto()
  ND = auto()
  OH = auto()
  OK = auto()
  OR = auto()
  MD = auto()
  MA = auto()
  MI = auto()
  MN = auto()
  MS = auto()
  MO = auto()
  PA = auto()
  RI = auto()
  SC = auto()
  SD = auto()
  TN = auto()
  TX = auto()
  UT = auto()
  VT = auto()
  VA = auto()
  WA = auto()
  WV = auto()
  WI = auto()
  WY = auto()   
