/** @odoo-module */

import publicWidget from 'web.public.widget';
import ajax from 'web.ajax';

publicWidget.registry.JobApplicationPortal = publicWidget.Widget.extend({
    selector: '#jobs_section',
    events: {
        'change #criminal_record': '_onChangeCriminalRec',
        'change #citizenship': '_onChangeCitizenship',
        'change #id_number': '_onChangeIdNumber',
        'change #disability': '_onChangeDisability',
    },

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        $('#id_number_field').show();
        $('#passport_field').hide();
        return def;
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onChangeCriminalRec: function (ev) {
        ev.preventDefault();
        var criminalRecordValue = $("select[name='criminal_record']").val();
        if (criminalRecordValue === 'Y') {
            $('#crime_info_div').show();
        } else {
            $('#crime_info_div').hide();
        }
    },

    _onChangeCitizenship: function (ev) {
        ev.preventDefault();
        var citizenshipVal = $("select[name='citizenship']").val();
        if (citizenshipVal === 'SA') {
            $('#id_number_field').show();
            $('#passport_field').hide();
        } else {
            $('#id_number_field').hide();
            $('#passport_field').show();
        }
    },

    _onChangeIdNumber: function (ev) {
        ev.preventDefault();
        var id_number = $("input[name='id_no']").val();
        ajax.jsonRpc('/validate/nationalityId', 'call', {'id_number': id_number})
        .then(function (result) {
            if (result == false){
                alert("Invalid Nationality ID");
            }
        })
    },

     _onChangeDisability: function (ev) {
        ev.preventDefault();
        var disabilityVal = $("select[name='disability']").val();
        if (disabilityVal === 'Y') {
            $('#disability_details_field').show();
        } else {
            $('#disability_details_field').hide();
        }
    },
});
