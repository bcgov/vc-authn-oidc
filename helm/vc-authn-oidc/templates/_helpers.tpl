{{/*
Expand the name of the chart.
*/}}
{{- define "vc-authn-oidc.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "vc-authn-oidc.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "vc-authn-oidc.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "vc-authn-oidc.labels" -}}
helm.sh/chart: {{ include "vc-authn-oidc.chart" . }}
{{ include "vc-authn-oidc.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "vc-authn-oidc.selectorLabels" -}}
app.kubernetes.io/name: {{ include "vc-authn-oidc.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
role: {{ .Values.role }}
{{- end }}

{{/*
Generate host name based on chart name + domain suffix
*/}}
{{- define "vc-authn-oidc.host" -}}
{{- include "vc-authn-oidc.fullname" . }}{{ .Values.global.ingressSuffix -}}
{{- end }}

{{/*
Add TLS annotation for OpenShift route
*/}}
{{- define "vc-authn-oidc.openshift.route.tls" -}}
{{- if (.Values.route.tls.enabled) -}}
tls:
  insecureEdgeTerminationPolicy: {{ .Values.route.tls.insecureEdgeTerminationPolicy }}
  termination: {{ .Values.route.tls.termination }}
{{- end -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "vc-authn-oidc.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "vc-authn-oidc.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create URL based on hostname and TLS status
*/}}
{{- define "vc-authn-oidc.url" -}}
{{- if or (eq .Values.route.tls.enabled true) (.Values.ingress.tls) }}
{{- printf "https://%s" (include "vc-authn-oidc.host" .) | quote }}
{{- else }}
{{- printf "http://%s" (include "vc-authn-oidc.host" .) | quote }}
{{- end }}
{{- end }}
