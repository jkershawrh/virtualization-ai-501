{{- define "virtualization-ai-501.labels" -}}
app.kubernetes.io/part-of: virtualization-ai-501
app.kubernetes.io/managed-by: {{ .Release.Service }}
lab.redhat.com/candidate: virtualization-ai-501
{{- end }}
{{- define "virtualization-ai-501.image" -}}
{{- if .digest -}}{{ .repository }}@{{ .digest }}{{- else -}}{{ .repository }}:{{ .tag }}{{- end -}}
{{- end }}
