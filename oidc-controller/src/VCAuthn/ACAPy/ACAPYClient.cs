using System;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.ACAPY
{
    public interface IACAPYClient
    {
        Task<WalletPublicDid> WalletDidPublic();
        string GetServicePublicUrl();
        Task<CreatePresentationResponse> CreatePresentationRequestAsync(PresentationRequestConfiguration configuration);
    }

    public class ACAPYClient : IACAPYClient
    {
        private readonly ILogger<ACAPYClient> _logger;
        private readonly string _baseUrl;
        private HttpClient _httpClient;
        
        public ACAPYClient(IConfiguration config, ILogger<ACAPYClient> logger)
        {
            _httpClient = new HttpClient();
            _logger = logger;
            _baseUrl = config.GetValue<string>("BaseUrl");
        }

        public string GetServicePublicUrl()
        {
            return _baseUrl;
        }

        public async Task<WalletPublicDid> WalletDidPublic()
        {
            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Get,
                RequestUri = new Uri($"{_baseUrl}{ACAPYConstants.WalletDidPublicUri}")
            };

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
                string json = JsonConvert.SerializeObject(configuration);
                var httpContent = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"{_baseUrl}{ACAPYConstants.PresentationExchangeCreateRequest}", httpContent);
                var responseContent = await response.Content.ReadAsStringAsync();

                _logger.LogDebug($"Status: [{response.StatusCode}], Content: [{responseContent}, Headers: [{response.Headers}]");

                switch (response.StatusCode)
                {
                    case HttpStatusCode.OK:
                        return JsonConvert.DeserializeObject<CreatePresentationResponse>(responseContent);
                    default:
                        throw new Exception($"Create presentation request error . Code: {response.StatusCode}");
                }
            }
            catch (Exception e)
            {
                throw new Exception("Create presentation request failed .", e);
            }
        }
    }
}