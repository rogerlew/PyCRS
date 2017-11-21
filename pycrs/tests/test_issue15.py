import pycrs

import unittest

class Issue15(unittest.TestCase):
    """
    inverse flattening for proj4 should be designated with +rf not +f
    """

    def test_parse_rf(self):
        proj4 = '+proj=lcc +lat_1=25.0 +lat_2=60.0 +lon_0=-100.0 +lat_0=42.5 '\
                '+a=6378137.0 +rf=298.257223563 +units=m +no_defs'
                
        fromcrs = pycrs.parser.from_unknown_text(proj4)
        tocrs = fromcrs.to_proj4()
        self.assertEqual(tocrs, 
            '+proj=lcc +a=6378137.0 +f=298.257223563 +pm=0  +lon_0=-100.0 +lat_0=42.5 +lat_1=25.0 +lat_2=60.0 +units=m +axis=enu +no_defs')
    
    def test_parse_f(self):
        proj4 = '+proj=lcc +lat_1=25.0 +lat_2=60.0 +lon_0=-100.0 +lat_0=42.5 '\
                '+a=6378137.0 +f=0.00335281066 +units=m +no_defs'
                
        fromcrs = pycrs.parser.from_unknown_text(proj4)
        tocrs = fromcrs.to_proj4()
        
        # rounding at 7th digit
        self.assertEqual(tocrs, 
            '+proj=lcc +a=6378137.0 +f=298.257223985 +pm=0  +lon_0=-100.0 +lat_0=42.5 +lat_1=25.0 +lat_2=60.0 +units=m +axis=enu +no_defs')
            
    def test_parse_wkt(self):
        wkt = 'PROJCS["Lambert_Conformal_Conic",'\
             'GEOGCS["GCS_Unknown",DATUM["D_Unknown",'\
             'SPHEROID["Unknown",6378137.0,298.257223563]],'\
             'PRIMEM["Greenwich",0],'\
             'UNIT["Degree",0.017453292519943295]],'\
             'PROJECTION["Lambert_Conformal_Conic"],'\
             'PARAMETER["Central_Meridian",-100.0],'\
             'PARAMETER["Latitude_Of_Origin",42.5],'\
             'UNIT["Meter",1.0],'\
             'PARAMETER["standard_parallel_1",42.5]]'
                
        fromcrs = pycrs.parser.from_unknown_text(wkt)
        tocrs = fromcrs.to_proj4()
        
        # prime meridian is in %.1f compared to previous tests
        self.assertEqual(tocrs, 
            '+proj=lcc +a=6378137.0 +f=298.257223563 +pm=0.0  +lon_0=-100.0 +lat_0=42.5 +lat_1=42.5 +units=m +axis=enu +no_defs')
    
if __name__ == '__main__':
    unittest.main()