def tablelout(fluxt_val_string, wline_val_string, snline_pspp_string, tsnline_pspp_string, snline_voxel_string, tsnline_voxel_string,
             snline_fibre1aa_string, tsnline_fibre1aa_string, snline_fibre_string, tsnline_fibre_string, snline_all_string, tsnline_all_string):
    tableloutstring = '<hr />' + \
                  'OUTPUT LINE SNR: ' + fluxt_val_string + \
                  '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
                  '<table border=1>' + \
                  '<tr>' \
                    '<th class="iconcolumn" scope="row"> </th>' \
                    '<td class="perframecolumn">per frame</td>' \
                    '<td class="allframecolumn">all frames</td>' \
                    '<td></td></tr>' + \
                  '<tr>' \
                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pdp.jpeg" /></td>' \
                    '<td class="perframecolumn"> ' + snline_pspp_string + '</td>' \
                    '<td> ' + tsnline_pspp_string + '</td>' \
                    '<td> per fiber per detector pixel</td></tr>' + \
                  '<tr>' \
                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
                    '<td class="perframecolumn"> ' + snline_voxel_string + '</td>' \
                    '<td> ' + tsnline_voxel_string + '</td>' \
                    '<td> per fiber per voxel</td></tr>' + \
                  '<tr>' \
                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_perfibinappang.jpeg" /></td>' \
                    '<td class="perframecolumn"> ' + snline_fibre1aa_string + '</td>' \
                    '<td> ' + tsnline_fibre1aa_string + '</td>' \
                    '<td> per fiber in aperture per AA</td></tr>' + \
                  '<tr>' \
                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_perfibinap.jpeg" /></td>' \
                    '<td class="perframecolumn"> ' + snline_fibre_string + '</td>' \
                    '<td> ' + tsnline_fibre_string + '</td>' \
                    '<td> per fiber in aperture</td></tr>' + \
                  '<tr>' \
                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_totalinap.jpeg" /></td>' \
                    '<td class="perframecolumn"> ' + snline_all_string + '</td>' \
                    '<td>' + tsnline_all_string + '</td>' \
                    '<td> total in aperture</td></tr>' + \
                  '</table><br />'
                  # '<tr>' \
                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pasqpang.jpeg" /></td>' \
                  #   '<td class="perframecolumn"> ' + snline_1_aa_string + '</td>' \
                  #   '<td> ' + tsnline_1_aa_string + '</td>' \
                  #   '<td> per arcsec per AA</td></tr>' + \
    return tableloutstring