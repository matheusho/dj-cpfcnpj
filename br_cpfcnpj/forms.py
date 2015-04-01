# coding: utf-8
import re

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


class BRCPFCNPJField(CharField):
    """
    A form field that validates input as `Brazilian CPF or CNPJ`_.

    CPF
    A form field that validates a CPF number or a CPF string. A CPF number is
    compounded by XXX.XXX.XXX-VD. The two last digits are check digits.
    More information:
    http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas

    CNPJ
    Input can either be of the format XX.XXX.XXX/XXXX-XX or be a group of 14
    digits.
    .. _Brazilian CNPJ: http://en.wikipedia.org/wiki/National_identification_number#Brazil
    """

    def __init__(self, min_length=11, *args, **kwargs):
        super(BRCPFCNPJField, self).__init__(min_length, *args, **kwargs)

    def clean(self, value):
        if len(value) <= 14:
            return self.cpf_valid(value)
        else:
            return self.cnpj_valid(value)

    def cpf_valid(self, value):
        """
        Value can be either a string in the format XXX.XXX.XXX-XX or an
        11-digit number.
        """
        error_messages = {
            'invalid': _("Invalid CPF number."),
            'max_digits': _("This field requires at most 11 digits or 14 characters."),
            'digits_only': _("This field requires only numbers."),
        }

        if value in EMPTY_VALUES:
            return ''
        orig_value = value[:]
        if not value.isdigit():
            value = re.sub("[-\. ]", "", value)
        try:
            int(value)
        except ValueError:
            raise ValidationError(error_messages['digits_only'])
        if len(value) != 11:
            raise ValidationError(error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx])
                       for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx])
                       for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(error_messages['invalid'])
        if value.count(value[0]) == 11:
            raise ValidationError(error_messages['invalid'])
        return orig_value

    def cnpj_valid(self, value):
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
        group of 14 characters.
        """
        error_messages = {
            'invalid': _("Invalid CNPJ number."),
            'digits_only': _("This field requires only numbers."),
            'max_digits': _("This field requires at least 14 digits"),
        }

        if value in EMPTY_VALUES:
            return ''
        orig_value = value[:]
        if not value.isdigit():
            value = re.sub("[-/\.]", "", value)
        try:
            int(value)
        except ValueError:
            raise ValidationError(error_messages['digits_only'])
        if len(value) != 14:
            raise ValidationError(error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx])
                       for idx, i in enumerate(list(range(5, 1, -1)) + list(range(9, 1, -1)))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx])
                       for idx, i in enumerate(list(range(6, 1, -1)) + list(range(9, 1, -1)))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(error_messages['invalid'])

        return orig_value
