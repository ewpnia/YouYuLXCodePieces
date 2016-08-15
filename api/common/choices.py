

class IDType(object):
    idcard = 'idcard'
    passport = 'passport'
    hk_macau_eep = 'hk_macau_eep' # "Valid Exit-Entry Permit (EEP) to HK / Macau"
    student_card = 'student_card'
    other = 'other'


class SexType(object):
    unknown = 'unknown'
    male    = 'male'
    female  = 'female'


class DevelopType(object):
    unknown = 'unknown'
    adult = 'adult'
    child = 'child'


class TransportationType(object):
    bus  = 'bus'
    train = 'train'
    airplan = 'airplan'
    steamship = 'steamship'
    