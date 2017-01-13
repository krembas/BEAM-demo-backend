import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class EvalView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            pyversion = subprocess.check_output(['python', '--version'], shell=False, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            pyversion = e.output
        pyversion = 'Evaluated with %sHere comes the results:\n' % pyversion.decode('utf-8')
        try:
            output = subprocess.check_output(['python', '-c', request.body.decode('utf-8')],
                                             shell=False, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        return HttpResponse('\n'.join([pyversion, output.decode('utf-8')]))
