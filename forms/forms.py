from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Fieldset, ButtonHolder, Div
from crispy_forms.bootstrap import UneditableField
from . import models
from django.contrib import messages

class PresentationForm(ModelForm):
    class Meta:
        model = models.Presentation
        fields = ['title', 'abstract', 'track', 'speaker']  
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout =Layout(
            HTML('<h2>Submit your session!!</h2>'),
        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field, wrapper_class='row')
            )
        helper.layout.append(Submit('submit','Submit your session', css_class='btn-success'))
        helper.field_class = 'col-md-4'
        helper.label_class = 'col-md-3'    
        return helper

class InspectionForm(ModelForm):
    class Meta:
        model = models.BPinspectionform
        fields = ['boolean','date_posted', 'serial_number', 'sample1', 'sample2', 'sample3', 'sample4','sample5','S1Sealing', 'S2Sealing', 'S3Sealing', 'S4Sealing', 'S5Sealing']
    
    @classmethod
    def save(self, *args, **kwargs):
        no_of_records=models.BPinspectionform.objects.all().count
        last_record=models.BPinspectionform.objects.get(id=no_of_records)
        ls=last_record.serial_number 

        if self.boolean == True:
            self.serial_number = ls+1
        else:
            self.serial_number = ls    
        super().save(*args, **kwargs) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            Fieldset(
                ' ',
                'boolean',
            ),
            Fieldset(
                ' ',
                'date_posted',
                ' ', css_class='row'
            ),    
            Fieldset(
                ' ',
                'sample1',
                'S1Sealing', css_class='row'
            ),
            Fieldset(
                ' ',
                'sample2',
                'S2Sealing', css_class='row'
            ),
            Fieldset(
                ' ',
                'sample3',
                'S3Sealing', css_class='row'
            ),
            Fieldset(
                ' ',
                'sample4',
                'S4Sealing', css_class='row'
            ),
            Fieldset(
                ' ',
                'sample5',
                'S5Sealing', css_class='row'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success')
            )
        )


class RTSForm(ModelForm):
    class Meta:
        model = models.RTSform
        fields = ['supplier', 'vehicle_number', 'dnote_number','dnote_date','material_description', 'quality_issue', 'reason_for_rejection', 'delivery_quantity', 'sampled_quantity', 'quantity_affected', 'acceptable_level','batches_sampled', 'mould']
        
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dnote_date'].widget.attrs.update({'placeholder': 'dd/mm/yyyy'})
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Div(HTML('<h3>Return To Supplier (R.T.S) Form </h3>'),css_class='center'),

            HTML("<hr>"),
            HTML("<hr>"),
            Div(
                Div(
                    #Div( UneditableField('date_posted', css_class='form-control-sm-2'), css_class='col-sm-'),
                    # Div('date_posted',css_class='col-sm-3',),

                    #Div('serial_number',css_class='col-sm-3',),

                    #Div('author',css_class='col-sm-3',),
                    Div(HTML('<h5>Department :  {{ request.user.profile.department }}</h5>'),css_class='col-sm-3'),
                    
                    # Div('department', css_class='col-sm-3'), 
                    
                    style="background: light;", css_class='row mb-3'
                ),

                HTML("<hr>"),
                HTML("<hr>"),

                HTML("<h5>Document Details</h5>"),

                Div(
                    Div('supplier', css_class='col-sm-4'),

                    Div('vehicle_number', css_class='col-sm-2'),
                    
                    Div('dnote_number', css_class='col-sm-2'),
                    
                    Div('dnote_date', css_class='col-sm-2'),

                    Div('delivery_quantity', css_class='col-sm-2'),
                    
                    style="background: white;", css_class='row mb-3', title="delivery"
                ),

                HTML("<hr>"),

                HTML("<h5>QC Findings</h5>"),

                Div(
                    Div('material_description', css_class='col-sm'),

                    Div('quality_issue', css_class='col-sm'),
                    
                    Div('reason_for_rejection', css_class='col-sm'),
                    
                    style="background: white;", css_class='row', title="delivery"
                ),

                Div(

                    Div('sampled_quantity', css_class='col-sm'),

                    Div('quantity_affected', css_class='col-sm'),

                    Div('acceptable_level', css_class='col-sm'),

                    Div('batches_sampled', css_class='col-sm'),

                    Div('mould', css_class='col-sm'),
                    
                    style="background: white;", css_class='row mb-2', title="delivery"
                ),
                HTML("<hr>")
            )
        ) 
        self.helper.layout.append(Submit('submit','Submit to HOD', css_class='btn-success'))

