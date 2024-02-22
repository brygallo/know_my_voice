from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import render_to_string
from weasyprint import HTML


class BasePDFView(View):
    template_name = ""
    download_filename = "document.pdf"
    open_in_browser = True

    def get_context_data(self, **kwargs):
        """
        This method must be overridden to return the necessary context for the template.
        """
        return {}

    def render_to_pdf_response(self, context):
        html_string = render_to_string(self.template_name, context)
        html = HTML(string=html_string)
        response = HttpResponse(content_type='application/pdf')
        content_disposition = 'inline' if self.open_in_browser else 'attachment'
        response['Content-Disposition'] = f'{content_disposition}; filename="{self.download_filename}"'
        html.write_pdf(response)
        return response

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_pdf_response(context)
