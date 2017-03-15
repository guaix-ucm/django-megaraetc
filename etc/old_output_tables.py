             # tablecoutstring = '<hr /><br />' + \
            #                   'OUTPUT CONTINUUM SNR:' + \
            #                   '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
            #                   '<table border=1>' + \
            #                   '<tr>' \
            #                     '<th class="iconcolumn" scope="col"> </th>' \
            #                     '<th scope="col" colspan="4">* SNR per fibre:</th>' \
            #                     '<th scope="col"></th></tr>' + \
            #                   '<tr>' \
            #                     '<th class="iconcolumn" scope="row"> </th>' \
            #                     '<td>npixx</td>' \
            #                     '<td>npixy</td>' \
            #                     '<td class="perframecolumn">per frame</td>' \
            #                     '<td class="allframecolumn">all frames</td>' \
            #                     '<td></td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pdp.jpeg" /></td>' \
            #                     '<td>' + npixx_pdp_fibre_string + '</td>' \
            #                     '<td>' + npixy_pdp_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_pdp_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_pdp_fibre_string + '</td>' \
            #                     '<td> per detector pixel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspp.jpeg" /></td>' \
            #                     '<td>' + npixx_psp_fibre_string + '</td>' \
            #                     '<td>' + npixy_psp_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_psp_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_psp_fibre_string + '</td>' \
            #                     '<td> per spectral pixel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
            #                     '<td>' + npixx_p2sp_fibre_string + '</td>' \
            #                     '<td>' + npixy_p2sp_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_p2sp_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_p2sp_fibre_string + '</td>' \
            #                     '<td> per voxel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
            #                     '<td>' + npixx_1aa_fibre_string + '</td>' \
            #                     '<td>' + npixy_1aa_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_1aa_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_1aa_fibre_string + '</td>' \
            #                     '<td> per AA</td></tr>' + \
            #                   '<tr class="rowheight">' \
            #                     '<td> </td></tr>' + \

            # tablecoutstring = '<hr />' + \
            #                   'OUTPUT CONTINUUM SNR:' + \
            #                   '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
            #                   '<table border=1>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"> </td>' \
            #                     '<th scope="col" colspan="4">* SNR in total source area:</th>' \
            #                     '<th>(number of fibers = ' + nfibres_string + ')</th></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"> </td>' \
            #                     '<td>npixx</td><td>npixy</td>' \
            #                     '<td class="perframecolumn">per frame</td>' \
            #                     '<td class="allframecolumn">all frames</td>' \
            #                     '<td></td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspp.jpeg" /></td>' \
            #                     '<td>' + npixx_psp_all_string + '</td>' \
            #                     '<td>' + npixy_psp_all_string + '</td>' \
            #                     '<td> ' + sncont_psp_all_string + ' </td>' \
            #                     '<td> ' + tsncont_psp_all_string + '</td>' \
            #                     '<td> per spectral pixel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
            #                     '<td>' + npixx_p2sp_all_string + '</td>' \
            #                     '<td>' + npixy_p2sp_all_string + '</td>' \
            #                     '<td> ' + sncont_pspfwhm_all_string + ' </td>' \
            #                     '<td> ' + tsncont_pspfwhm_all_string + '</td>' \
            #                     '<td> per voxel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
            #                     '<td>' + npixx_1aa_all_string + '</td>' \
            #                     '<td>' + npixy_1aa_all_string + '</td>' \
            #                     '<td> ' + sncont_1aa_all_string + ' </td>' \
            #                     '<td> ' + tsncont_1aa_all_string + '</td>' \
            #                     '<td> per AA</td></tr>' + \
            #                   '</table><br />'

            # if sourcet_val_string == 'E':
            #                       # '<hr />' + \
            #                       # 'OUTPUT CONTINUUM <br />' + \
            #                       # '(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
            #     tablecoutstring = tablecoutstring + \
            #                       '<hr />' + \
            #                       '<table border=1>' + \
            #                       '<tr>' \
            #                         '<th class="iconcolumn" scope="col"> </td>' \
            #                         '<th scope="col" colspan="4">* SNR in one seeing:</th><th scope="col"></th></tr>' + \
            #                       '<tr>' \
            #                         '<th class="iconcolumn" scope="row"> </th>' \
            #                         '<td>npixx</td>' \
            #                         '<td>npixy</td>' \
            #                         '<td class="perframecolumn">per frame</td>' \
            #                         '<td class="allframecolumn">all frames</td>' \
            #                         '<td></td></tr>' + \
            #                       '<tr>' \
            #                         '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
            #                         '<td>' + npixx_p2sp_seeing_string + '</td>' \
            #                         '<td>' + npixy_p2sp_seeing_string + '</td>' \
            #                         '<td> ' + sncont_p2sp_seeing_string + ' </td>' \
            #                         '<td> ' + tsncont_p2sp_seeing_string + '</td>' \
            #                         '<td> per voxel</td></tr>' + \
            #                       '<tr>' \
            #                         '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
            #                         '<td>' + npixx_1aa_seeing_string + '</td>' \
            #                         '<td>' + npixy_1aa_seeing_string + '</td>' \
            #                         '<td> ' + sncont_1aa_seeing_string + ' </td>' \
            #                         '<td> ' + tsncont_1aa_seeing_string + '</td>' \
            #                         '<td> per AA</td></tr>' + \
            #                       '<tr>' \
            #                         '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' \
            #                         '<td>' + npixx_band_seeing_string + '</td>' \
            #                         '<td>' + npixy_band_seeing_string + '</td>' \
            #                         '<td> ' + sncont_band_seeing_string + ' </td>' \
            #                         '<td> ' + tsncont_band_seeing_string + '</td>' \
            #                         '<td> per integrated spectrum (spaxel)</td></tr>' + \
            #                       '</table>'
                                  # '<tr class="rowheight">' \
                                  #   '<td> </td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"> </td>' \
                                  #   '<th scope="col" colspan="4">* SNR in one arcsec^2:</th>' \
                                  #   '<th></th></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"> </td>' \
                                  #   '<td>npixx</td>' \
                                  #   '<td>npixy</td>' \
                                  #   '<td class="perframecolumn">per frame</td>' \
                                  #   '<td class="allframecolumn">all frames</td>' \
                                  #   '<td></td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
                                  #   '<td>' + npixx_p2sp_1_string + '</td>' \
                                  #   '<td>' + npixy_p2sp_1_string + '</td>' \
                                  #   '<td> ' + sncont_p2sp_1_string + ' </td>' \
                                  #   '<td> ' + tsncont_p2sp_1_string + '</td>' \
                                  #   '<td> per voxel</td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
                                  #   '<td>' + npixx_1aa_1_string + '</td>' \
                                  #   '<td>' + npixy_1aa_1_string + '</td>' \
                                  #   '<td> ' + sncont_1aa_1_string + ' </td>' \
                                  #   '<td> ' + tsncont_1aa_1_string + '</td>' \
                                  #   '<td> per AA</td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' \
                                  #   '<td>' + npixx_band_1_string + '</td>' \
                                  #   '<td>' + npixy_band_1_string + '</td>' \
                                  #   '<td> ' + sncont_band_1_string + ' </td>' \
                                  #   '<td> ' + tsncont_band_1_string + '</td>' \
                                  #   '<td> per integrated spectrum (spaxel)</td></tr>' + \
                                  # '</table>'


                                              # TABLES NEWPSF LINE (ATTEMPT; TBD)
            # if om_val_string == 'MOS' and fluxt_val_string == 'L' and sourcet_val_string == 'E':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                         '<table border=1>' + \
            #                         '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                             '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                             '(MOS mode) for an extended source:<br />' + \
            #                             'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                             '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                             '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                             '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area <br />' + nfibres_string + ' fibers</td>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                             '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area<br />' + nfibres_string + ' fibers</td>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per voxel</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per AA</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> integrated spectrum </td>' + \
            #                             '</tr>' + \
            #                         '</table><br />'
            # elif om_val_string == 'MOS' and fluxt_val_string == 'L' and sourcet_val_string == 'P':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                             '<table border=1>' + \
            #                             '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                                 '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                                 '(MOS mode) for a point source:<br />' + \
            #                                 'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec <br />'
            #     if resolvedline_val_string == 'N':
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'line FWHM = VPH FWHM = ' + fwhmline_val_string + '</th>'
            #     else:
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'input line FWHM = ' + fwhmline_val_string + '</th>'
            #     tablenewpsflinestring = tablenewpsflinestring + \
            #                             '</tr>' + \
            #                             '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                                 '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                                 '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                                 '<td></td>' + \
            #                                 '</tr>' + \
            #                             '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                                 '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                                 '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                                 '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area <br />' + nfibres_string + ' fibers</td>' + \
            #                                 '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                                 '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                                 '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area<br />' + nfibres_string + ' fibers</td>' + \
            #                                 '<td></td>' + \
            #                                 '</tr>' + \
            #                             '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                                 '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                                 '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                                 '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td> per voxel</td>' + \
            #                                 '</tr>' + \
            #                             '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                                 '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                                 '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                                 '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td> per AA</td>' + \
            #                                 '</tr>' + \
            #                             '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                                 '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                                 '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                                 '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td> integrated spectrum </td>' + \
            #                                 '</tr>' + \
            #                             '</table><br />'
            # elif om_val_string == 'LCB' and fluxt_val_string == 'L' and sourcet_val_string == 'E':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                         '<table border=1>' + \
            #                         '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                             '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                             '(LCB mode) for an extended source:<br />' + \
            #                             'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                             '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                             '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td>percentage of enclosed total flux</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per voxel</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per AA</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> integrated spectrum </td>' + \
            #                             '</tr>' + \
            #                         '</table><br />'
            # elif om_val_string == 'LCB' and fluxt_val_string == 'L' and sourcet_val_string == 'P':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                         '<table border=1>' + \
            #                         '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                             '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                             '(LCB mode) for a point source:<br />' + \
            #                             'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec<br />'
            #     if resolvedline_val_string == 'N':
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'line FWHM = VPH FWHM = ' + fwhmline_val_string + '</th>'
            #     else:
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'input line FWHM = ' + fwhmline_val_string + '</th>'
            #     tablenewpsflinestring = tablenewpsflinestring + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                             '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                             '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td>percentage of enclosed total flux</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per voxel</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per AA</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> integrated spectrum </td>' + \
            #                             '</tr>' + \
            #                         '</table><br />'
            # else:
            #     tablenewpsflinestring = "no line output"