bandc_list = ['U', 'B', 'V', 'R', 'I']
filterc_list = ['FILTERS_0.1aa/u_johnsonbessel.dat','FILTERS_0.1aa/b_johnsonbessel.dat',
                    'FILTERS_0.1aa/v_johnsonbessel.dat','FILTERS_0.1aa/r_johnsonbessel.dat',
                    'FILTERS_0.1aa/i_johnsonbessel.dat']

    # Central Wavelength and width of filters.
filterchar_list = [(3657.5, 577.0, 3369.0, 3946.),   # For Johnson-Cousins U-band
                       (4334.5, 975.0, 3847., 4822.),   # For Johnson-Cousins B-band
                       (5374.0, 846.0, 4951., 5797.),   # For Johnson-Cousins V-band
                       (6272.5, 1273.0, 5635.5, 6909.),  # For Johnson-Cousins R-band
                       (8722.0, 2980.0, 7232., 10212.)]  # For Johnson-Cousins I-band

vegachar = [(0.030,4.22e-9),   # For Johnson-Cousins U-band
                (0.035,6.20e-9),   # For Johnson-Cousins B-band
                (0.035,3.55e-9),   # For Johnson-Cousins V-band
                (0.075,1.795e-9),  # For Johnson-Cousins R-band
                (0.095,8.60e-9)]   # For Johnson-Cousins I-band

fix = []
i = 0
for x in vegachar:
    fields = {}
    fields['name'] = bandc_list[i]
    fields['path'] = filterc_list[i]
    fields['cwl'] = filterchar_list[i][0]
    fields['width'] = filterchar_list[i][1]
    fields['lambda_b'] = filterchar_list[i][2]
    fields['lambda_e'] = filterchar_list[i][3]
    fields['mvega'] = vegachar[i][0]
    fields['fvega'] = vegachar[i][1]
    entry = {'model': 'etc.photometricfilter',
             'pk': i+1,
             'fields': fields,
             }
    fix.append(entry)
    i += 1

import json

json.dump(fix, open('filter_fixture.json', 'wb'))
