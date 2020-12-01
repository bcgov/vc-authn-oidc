using IdentityServer4.Hosting;
using IdentityServer4.Extensions;
using Microsoft.AspNetCore.Http;
using System;
using System.Threading.Tasks;

namespace VCAuthn.IdentityServer.Endpoints.AuthorizeCallbackEndpoint
{
    public class AuthorizeCallbackResult : IEndpointResult
    {
        private readonly string _url;

        public AuthorizeCallbackResult(string url)
        {
            if (string.IsNullOrWhiteSpace(url)) throw new ArgumentNullException(nameof(url));

            _url = url;
        }

        public async Task ExecuteAsync(HttpContext context)
        {
            context.Response.RedirectToAbsoluteUrl(_url);

            await Task.CompletedTask;
        }
    }
}
