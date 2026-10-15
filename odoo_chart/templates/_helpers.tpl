<! =>> {*Helm Template Helper Functions*} =>>
{{- define "odoo.fullname" -}}
{{ .Release.Name }}-odoo
{{- end }}