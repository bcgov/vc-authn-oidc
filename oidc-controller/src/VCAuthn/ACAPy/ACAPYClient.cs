using System;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using VCAuthn.Models;
using VCAuthn.Utils;

namespace VCAuthn.ACAPY
{
    public interface IACAPYClient
    {
        Task<WalletPublicDid> WalletDidPublic();
        string GetAdminUrl();
        string GetAgentUrl();
        Task<CreatePresentationResponse> CreatePresentationRequestAsync(PresentationRequestConfiguration configuration);
    }

    public class ACAPYClient : IACAPYClient
    {
        private readonly ILogger<ACAPYClient> _logger;
        private readonly string _adminUrl;
        private readonly string _adminUrlApiKey;

        private readonly string _agentUrl;
        private HttpClient _httpClient;

        public ACAPYClient(IConfiguration config, ILogger<ACAPYClient> logger)
        {
            _httpClient = new HttpClient();
            _logger = logger;
            _adminUrl = config.GetValue<string>("AdminUrl");
            _adminUrlApiKey = config.GetValue<string>("AdminUrlApiKey");
            _agentUrl = config.GetValue<string>("AgentUrl");
        }

        public string GetAdminUrl()
        {
            return _adminUrl;
        }

        public string GetAgentUrl()
        {
            return _agentUrl;
        }

        public async Task<WalletPublicDid> WalletDidPublic()
        {
            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Get,
                RequestUri = new Uri($"{_adminUrl}{ACAPYConstants.WalletDidPublicUri}")
            };

            if (!string.IsNullOrEmpty(_adminUrlApiKey))
            {
                request.Headers.Add(ACAPYConstants.ApiKeyHeader, _adminUrlApiKey);
            }

            try
            {
                var response = await _httpClient.SendAsync(request);
                var responseContent = await response.Content.ReadAsStringAsync();

                _logger.LogDebug($"Status: [{response.StatusCode}], Content: [{responseContent}, Headers: [{response.Headers}]");

                switch (response.StatusCode)
                {
                    case HttpStatusCode.OK:
                        return JsonConvert.DeserializeObject<WalletDidPublicResponse>(responseContent).Result;
                    default:
                        throw new Exception($"Wallet Did public request error. Code: {response.StatusCode}");
                }
            }
            catch (Exception e)
            {
                throw new Exception("Wallet Did public request failed.", e);
            }
        }

        public async Task<CreatePresentationResponse> CreatePresentationRequestAsync(PresentationRequestConfiguration configuration)
        {
            try
            {
                // Build appropriate json request body
                string jsonRequestBody = configuration.GeneratePresentationRequest();

                var httpContent = new StringContent(jsonRequestBody, Encoding.UTF8, "application/json");
                if (!string.IsNullOrEmpty(_adminUrlApiKey))
                {
                    httpContent.Headers.Add(ACAPYConstants.ApiKeyHeader, _adminUrlApiKey);
                }

                var response = await _httpClient.PostAsync($"{_adminUrl}{ACAPYConstants.PresentProofCreateRequest}", httpContent);
                var responseContent = await response.Content.ReadAsStringAsync();

                _logger.LogDebug($"Status: [{response.StatusCode}], Content: [{responseContent}, Headers: [{response.Headers}]");

                switch (response.StatusCode)
                {
                    case HttpStatusCode.OK:
                        return JsonConvert.DeserializeObject<CreatePresentationResponse>(responseContent);
                    default:
                        throw new Exception($"Code: [{response.StatusCode}], Reason: [{responseContent}]");
                }
            }
            catch (Exception e)
            {
                throw new Exception($"Create presentation request failed: {e.Message}", e);
            }
        }
    }
}