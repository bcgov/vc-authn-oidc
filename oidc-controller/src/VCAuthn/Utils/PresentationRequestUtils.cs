using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.Utils
{
    public static class PresentationRequestUtils
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

        public static List<PresentationAttachment> GeneratePresentationAttachments(PresentationRequest presentationRequest) {
            List<PresentationAttachment> attachments = new List<PresentationAttachment>();

            string base64Payload = presentationRequest.ToJson().ToBase64();

            PresentationAttachment attachment = new PresentationAttachment();
            attachment.Id = "libindy-request-presentation-0"; 
            attachment.MimeType = "application/json";
            attachment.Data = new Dictionary<string, string>();
            attachment.Data.Add("base64", base64Payload);

            attachments.Add(attachment);
            
            return attachments;
        }

        /// <summary> Utility function that extracts the first Indy <c>Presentationrequest</c> object found
        /// in the provided list of <c>PresentationAttachment</c> objects. The Indy <c>Presentationrequest</c>
        /// is identified by <c>"@id": "libindy-request-presentation-0"</c>, as specified in the Aries RFC 0037.
        /// <see cref="https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof#request-presentation"/> 
        /// </summary>
        public static PresentationRequest ExtractIndyPresentationPequest(List<PresentationAttachment> presentationAttachments) {
            PresentationRequest presentationRequest = null;
            
            foreach (PresentationAttachment attachment in presentationAttachments) {
                if (attachment.Id.Equals("libindy-request-presentation-0")) {
                    // found first indy presentation attachment, deserialize it so thatit can be returned
                    string attachmentData = attachment.Data["base64"].FromBase64();
                    presentationRequest = JsonConvert.DeserializeObject<PresentationRequest>(attachmentData);
                }
            }
            
            return presentationRequest;
        }
    }

    
}