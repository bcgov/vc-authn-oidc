using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.Utils
{
    public static class ProofRequestUtils
    {
        public static string GenerateProofRequest(PresentationRequestConfiguration configuration)
        {
            ProofRequest_v_1_0 proofRequest_1_0 = new ProofRequest_v_1_0();
            proofRequest_1_0.Version = configuration.Version;
            proofRequest_1_0.Name = configuration.Name;

            foreach (RequestedAttribute reqAttribute in configuration.RequestedAttributes) {
                proofRequest_1_0.RequestedAttributes.Add(Guid.NewGuid().ToString(), reqAttribute);
            }
            foreach (RequestedPredicate reqPredicate in configuration.RequestedPredicates) {
                proofRequest_1_0.RequestedPredicates.Add(Guid.NewGuid().ToString(), reqPredicate);
            }

            Dictionary<string, ProofRequest_v_1_0> requestBody = new Dictionary<string, ProofRequest_v_1_0>();
            requestBody.Add("proof_request", proofRequest_1_0);
            return JsonConvert.SerializeObject(requestBody);
        }
    }

    
}