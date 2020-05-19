using System;
using System.IO;
using System.Threading.Tasks;
using IdentityServer4.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Abstractions;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using Microsoft.AspNetCore.Mvc.Razor;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Microsoft.AspNetCore.Routing;
using Microsoft.Extensions.DependencyInjection;
using VCAuthn.Models;

namespace VCAuthn.IdentityServer.Endpoints
{
    public class AuthorizationViewModel
    {
        public string Challenge { get; }
        public string PollUrl { get; }
        public string ResolutionUrl { get; }
        public int Interval { get; }

        public string PresentationRequest { get; }

        public AuthorizationViewModel(string challenge, string pollUrl, string resolutionUrl, string presentationRequest = null)
        {
            Challenge = challenge;
            PollUrl = pollUrl;
            ResolutionUrl = resolutionUrl;
            PresentationRequest = presentationRequest;
            Interval = 2000;
        }
    }

    public class AuthorizationEndpointResult : IEndpointResult
    {
        private readonly AuthorizationViewModel _authorizationRequest;
        private readonly string _viewName = IdentityConstants.AuthorizationViewName;

        public AuthorizationEndpointResult(AuthorizationViewModel authorizationRequest)
        {
            _authorizationRequest = authorizationRequest;
        }

        public async Task ExecuteAsync(HttpContext context)
        {
            var _viewEngine = context.RequestServices.GetRequiredService<IRazorViewEngine>();
            var _tempDataProvider = context.RequestServices.GetRequiredService<ITempDataProvider>();

            using (var sw = new StringWriter())
            {
                var actionContext = new ActionContext(context, new RouteData(), new ActionDescriptor());
                var viewResult = _viewEngine.GetView(_viewName, _viewName, false);

                if (viewResult.View == null)
                {
                    throw new ArgumentNullException($"{_viewName} does not match any available view");
                }
 
                var viewDictionary = new ViewDataDictionary(new EmptyModelMetadataProvider(), new ModelStateDictionary())
                {
                    Model = _authorizationRequest
                };
 
                var viewContext = new ViewContext(
                    actionContext,
                    viewResult.View,
                    viewDictionary,
                    new TempDataDictionary(context, _tempDataProvider),
                    sw,
                    new HtmlHelperOptions()
                );
 
                await viewResult.View.RenderAsync(viewContext);
                await context.Response.WriteHtmlAsync(sw.ToString());
            }
        }
    }
}