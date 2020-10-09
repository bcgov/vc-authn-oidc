using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using Microsoft.AspNetCore.Http;

namespace VCAuthn.IdentityServer.Endpoints
{
    public static class VCResponseHelpers
    {
        public static VCErrorResult Error(string error, string errorDescription = null)
        {
            var response = new VCErrorResponse
            {
                Error = error,
                ErrorDescription = errorDescription
            };

            return new VCErrorResult(response);
        }
    }

    /// <summary>
    /// Models a verified credential error response
    /// </summary>
    public class VCErrorResponse
    {
        public string Error { get; set; } = OidcConstants.TokenErrors.InvalidRequest;

        public string ErrorDescription { get; set; }
    }

    public class VCErrorResult : IEndpointResult
    {
        public VCErrorResponse Response { get; }

        public VCErrorResult(VCErrorResponse error)
        {
            Response = error;
        }

        public async Task ExecuteAsync(HttpContext context)
        {
            context.Response.StatusCode = 400;
            context.Response.SetNoCache();

            var dto = new ResultDto
            {
                error = Response.Error,
                error_description = Response.ErrorDescription
            };

            await context.Response.WriteJsonAsync(dto);
        }

        internal class ResultDto
        {
            public string error { get; set; }
            public string error_description { get; set; }
        }
    }
}