using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.Models
{
    public class AuthSession
    {
        public string Id { get; set; }

        public DateTime ExpiredTimestamp { get; set; }

        public string PresentationRecordId { get; set; }

        public string PresentationRequestId { get; set; }

        public bool PresentationRequestSatisfied { get; set; }

        // exists to convince EntityFramework to store request parameters as a string
        private string _requestParameters;

        [NotMapped]
        public Dictionary<string,string> RequestParameters
        {
            get => _requestParameters == null ? null : JsonConvert.DeserializeObject<Dictionary<string,string>>(_requestParameters);
            set => _requestParameters = JsonConvert.SerializeObject(value);
        }

        private string _presentationRequest;

        [NotMapped]
        public PresentationRequest PresentationRequest
        {
            get => _presentationRequest == null ? null : JsonConvert.DeserializeObject<PresentationRequest>(_presentationRequest);
            set => _presentationRequest = JsonConvert.SerializeObject(value);
        }

        // exists to convince EntityFramework to store presentation as a string
        private string _presentation;

        [NotMapped]
        public Presentation Presentation
        {
            get => _presentation == null ? null : JsonConvert.DeserializeObject<Presentation>(_presentation);
            set => _presentation = JsonConvert.SerializeObject(value);
        }
    }
    
    
}