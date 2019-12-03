using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.Utils
{
    public static class ProofRequestUtils
    {
        public static string GeneratePresentationRequest(PresentationRequestConfiguration configuration)
        {
            PresentationRequest_v_1_0 presentationRequest_1_0 = new PresentationRequest_v_1_0();
            presentationRequest_1_0.Version = configuration.Version;
            presentationRequest_1_0.Name = configuration.Name;

            foreach (RequestedAttribute reqAttribute in configuration.RequestedAttributes) {
                presentationRequest_1_0.RequestedAttributes.Add(Guid.NewGuid().ToString(), reqAttribute);
            }
            foreach (RequestedPredicate reqPredicate in configuration.RequestedPredicates) {
                presentationRequest_1_0.RequestedPredicates.Add(Guid.NewGuid().ToString(), reqPredicate);
            }

            Dictionary<string, PresentationRequest_v_1_0> requestBody = new Dictionary<string, PresentationRequest_v_1_0>();
            requestBody.Add("proof_request", presentationRequest_1_0);
            return JsonConvert.SerializeObject(requestBody);
        }

        public static string GeneratePresentationAttachments(PresentationRequest presentationRequest) {
            List<PresentationAttachment> attachments = new List<PresentationAttachment>();

            string base64Payload = presentationRequest.ToJson().ToBase64();

            PresentationAttachment attachment = new PresentationAttachment();
            attachment.Id = Guid.NewGuid().ToString();
            attachment.MimeType = "application/json";
            attachment.Data = new Dictionary<string, string>();
            attachment.Data.Add("base64", base64Payload);

            attachments.Add(attachment);
            
            return JsonConvert.SerializeObject(attachments);
        }
    }

    
}