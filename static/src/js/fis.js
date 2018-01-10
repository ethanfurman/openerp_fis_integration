openerp_FieldMany2ManyTagsEmail = function(instance) {
var _t = instance.web._t;

instance.web.form.NegativeFloatOkay = instance.web.form.FieldFloat.extend({

    render_value: function() {
        var value_okay = this.get('value') <= 0;
        var show_value = this.format_value(this.get('value'), '');
        console.log('zero_value is', this.options);
        var zero_value = this.options.zero_value || '0'
        if (!this.get("effective_readonly")) {
            this.$el.find('input').val(show_value);
        } else {
            this.$(".oe_form_char_content").text(zero_value);
        }
        if (value_okay) {
            this.$el.removeClass("fis_red");
        } else {
            this.$el.addClass("fis_red");
        }
    },

});

instance.web.form.PositiveFloatOkay = instance.web.form.FieldFloat.extend({

    render_value: function() {
        var value_okay = this.get('value') >= 0;
        var show_value = this.format_value(this.get('value'), '');
        console.log('zero_value is', this.options);
        var zero_value = this.options.zero_value || '0'
        if (!this.get("effective_readonly")) {
            this.$el.find('input').val(show_value);
        } else {
            this.$(".oe_form_char_content").text(zero_value);
        }
        if (value_okay) {
            this.$el.removeClass("fis_red");
        } else {
            this.$el.addClass("fis_red");
        }
    },

});


/**
 * Registry of form fields
 */
instance.web.form.widgets = instance.web.form.widgets.extend({
    'fis_negative_okay' : 'instance.web.form.NegativeFloatOkay',
    'fis_positive_okay' : 'instance.web.form.PositiveFloatOkay',
});

};

