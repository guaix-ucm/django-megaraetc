def tablenewpsfLPS(snr_string, numframe_val_string, snrpframe_string,
exptimepframe_string, exptimeval_string,
etpframe_c_voxel_string, etallframe_c_voxel_string,
etpframe_cr1_voxel_string, etallframe_cr1_voxel_string,
etpframe_cr1r2_voxel_string, etallframe_cr1r2_voxel_string,
etpframe_c_aa_string, etallframe_c_aa_string,
etpframe_cr1_aa_string, etallframe_cr1_aa_string,
etpframe_cr1r2_aa_string, etallframe_cr1r2_aa_string,
etpframe_c_all_string, etallframe_c_all_string,
etpframe_cr1_all_string, etallframe_cr1_all_string,
etpframe_cr1r2_all_string, etallframe_cr1r2_all_string,
lambdaeff_string, seeingx_string,
sncont_centerspaxel_voxel_string, sncont_cr1spaxels_voxel_string, sncont_cr1r2spaxels_voxel_string,
tsncont_centerspaxel_voxel_string, tsncont_cr1spaxels_voxel_string, tsncont_cr1r2spaxels_voxel_string,
sncont_centerspaxel_aa_string, sncont_cr1spaxels_aa_string, sncont_cr1r2spaxels_aa_string,
tsncont_centerspaxel_aa_string, tsncont_cr1spaxels_aa_string, tsncont_cr1r2spaxels_aa_string,
sncont_centerspaxel_all_string, sncont_cr1spaxels_all_string, sncont_cr1r2spaxels_all_string,
tsncont_centerspaxel_all_string, tsncont_cr1spaxels_all_string, tsncont_cr1r2spaxels_all_string):
    tablenewpsfstring = '<hr />' + \
                    'OUTPUT CONTINUUM EXPOSURE TIME' + \
                    '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
                    '<table border=1>' + \
                    '<tr><th class="iconcolumn" scope="col"> </th>' + \
                        '<th scope="col" colspan="7">* Exptime to reach input SNR ('+ snr_string +') per spaxel zones due to PSF (LCB mode):<br />' + \
                        'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec<br />' + \
                        'Unit: second</th>' + \
                        '</tr>' + \
                    '<tr><th class="iconcolumn" scope="row"></th>' + \
                        '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
                        '<th scope="col" colspan="3" class="allframecolumn">** all frames ('+ numframe_val_string+')</th>' + \
                        '<td></td>' + \
                        '</tr>' + \
                    '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
                        '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />19 fibers</td>' + \
                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
                        '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />19 fibers</td>' + \
                        '<td></td>' + \
                        '</tr>' + \
                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
                        '<td class="perframecolumn"> ' + etpframe_c_voxel_string + ' </td>' + \
                        '<td> ' + etpframe_cr1_voxel_string + '</td>' + \
                        '<td> ' + etpframe_cr1r2_voxel_string + '</td>' + \
                        '<td class="perframecolumn"> ' + etallframe_c_voxel_string + ' </td>' + \
                        '<td> ' + etallframe_cr1_voxel_string + '</td>' + \
                        '<td> ' + etallframe_cr1r2_voxel_string + '</td>' + \
                        '<td> per voxel</td>' + \
                        '</tr>' + \
                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
                        '<td class="perframecolumn"> ' + etpframe_c_aa_string + ' </td>' + \
                        '<td> ' + etpframe_cr1_aa_string + '</td>' + \
                        '<td> ' + etpframe_cr1r2_aa_string + '</td>' + \
                        '<td class="perframecolumn"> ' + etallframe_c_aa_string + ' </td>' + \
                        '<td> ' + etallframe_cr1_aa_string + '</td>' + \
                        '<td> ' + etallframe_cr1r2_aa_string + '</td>' + \
                        '<td> per AA</td>' + \
                        '</tr>' + \
                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
                        '<td class="perframecolumn"> ' + etpframe_c_all_string + ' </td>' + \
                        '<td> ' + etpframe_cr1_all_string + '</td>' + \
                        '<td> ' + etpframe_cr1r2_all_string + '</td>' + \
                        '<td class="perframecolumn"> ' + etallframe_c_all_string + ' </td>' + \
                        '<td> ' + etallframe_cr1_all_string + '</td>' + \
                        '<td> ' + etallframe_cr1r2_all_string + '</td>' + \
                        '<td> integrated spectrum </td>' + \
                        '</tr>' + \
                        '</table><br />'
    return tablenewpsfstring