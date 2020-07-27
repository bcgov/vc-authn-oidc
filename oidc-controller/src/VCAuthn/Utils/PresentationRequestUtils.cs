using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.Utils
{
    public static class PresentationRequestUtils
    {
        public static string GeneratePresentationRequest(this PresentationRequestConfiguration configuration)
        {
            PresentationRequest_v_1_0 presentationRequest_1_0 = new PresentationRequest_v_1_0()
            {
                Version = configuration.Version,
                Name = configuration.Name
                // NonRevoked = new RevocationInterval()
                // {
                //     From = 0,
                //     To = new DateTimeOffset(DateTime.Now, TimeSpan.Zero).ToUnixTimeSeconds()
                // }
            };

            configuration.RequestedAttributes.ForEach(delegate (RequestedAttribute reqAttribute)
            {
                string referent = !String.IsNullOrEmpty(reqAttribute.Label) ? reqAttribute.Label : Guid.NewGuid().ToString();
                reqAttribute.Label = null; // purge unsupported value from object that will be sent to aca-py
                if (!presentationRequest_1_0.RequestedAttributes.ContainsKey(referent))
                {
                    presentationRequest_1_0.RequestedAttributes.Add(referent, reqAttribute);
                }
                else
                {
                    presentationRequest_1_0.RequestedAttributes.Add(disambiguateReferent(referent), reqAttribute);
                }
            });

            configuration.RequestedPredicates.ForEach(delegate (RequestedPredicate reqPredicate)
            {
                string referent = !String.IsNullOrEmpty(reqPredicate.Label) ? reqPredicate.Label : Guid.NewGuid().ToString();
                reqPredicate.Label = null; // purge unsupported value from object that will be sent to aca-py
                if (!presentationRequest_1_0.RequestedPredicates.ContainsKey(referent))
                {
                    presentationRequest_1_0.RequestedPredicates.Add(referent, reqPredicate);
                }
                else
                {
                    presentationRequest_1_0.RequestedPredicates.Add(disambiguateReferent(referent), reqPredicate);
                }
            });

            Dictionary<string, PresentationRequest_v_1_0> requestBody = new Dictionary<string, PresentationRequest_v_1_0>()
            {
                {"proof_request", presentationRequest_1_0}
            };
            return JsonConvert.SerializeObject(requestBody, new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore });
        }

        public static List<PresentationAttachment> GeneratePresentationAttachments(this PresentationRequest presentationRequest)
        {
            string base64Payload = presentationRequest.ToJson().ToBase64();
            PresentationAttachment attachment = new PresentationAttachment()
            {
                Id = "libindy-request-presentation-0",
                MimeType = "application/json",
                Data = new Dictionary<string, string>()
                {
                    {"base64", base64Payload}
                },
            };

            return new List<PresentationAttachment>()
            {
                attachment
            };
        }

        /// <summary> Utility function that extracts the first Indy <c>Presentationrequest</c> object found
        /// in the provided list of <c>PresentationAttachment</c> objects. The Indy <c>Presentationrequest</c>
        /// is identified by <c>"@id": "libindy-request-presentation-0"</c>, as specified in the Aries RFC 0037.
        /// <see cref="https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof#request-presentation"/> 
        /// </summary>
        public static PresentationRequest ExtractIndyPresentationRequest(this List<PresentationAttachment> presentationAttachments)
        {
            PresentationRequest presentationRequest = null;

            presentationAttachments.ForEach(delegate (PresentationAttachment attachment)
            {
                if (attachment.Id.Equals("libindy-request-presentation-0"))
                {
                    // found first indy presentation attachment, deserialize it so that it can be returned
                    presentationRequest = attachment.Data["base64"].toPresentationRequestObject();
                }
            });

            return presentationRequest;
        }

        public static PresentationRequest toPresentationRequestObject(this string attachmentBase64Data)
        {
            return JsonConvert.DeserializeObject<PresentationRequest>(attachmentBase64Data.FromBase64());
        }

        private static String disambiguateReferent(this string referent)
        {
            int refIdx = 1;
            if (referent.Split("~").Length > 1)
            {
                string[] splitReferent = referent.Split("~");
                int oldIdx = Int32.Parse(splitReferent[splitReferent.Length - 1]);
                refIdx += oldIdx;
            }
            return $"{referent}~{refIdx}";
        }
    }


}