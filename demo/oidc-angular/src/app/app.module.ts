import { BrowserModule } from '@angular/platform-browser';
import {APP_INITIALIZER, NgModule} from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HomeComponent } from './home/home.component';
import {
  AuthModule,
  ConfigResult,
  OidcConfigService,
  OidcSecurityService,
  OpenIdConfiguration
} from 'angular-auth-oidc-client';

const OIDC_CONFIGURATION = 'assets/auth.clientConfiguration.json';

export function loadConfig(oidcConfigService: OidcConfigService) {
  return () => oidcConfigService.load(OIDC_CONFIGURATION);
}

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
    AuthModule.forRoot(),
  ],
  providers: [
    OidcConfigService,
    {
      provide: APP_INITIALIZER,
      useFactory: loadConfig,
      deps: [OidcConfigService],
      multi: true,
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(private oidcSecurityService: OidcSecurityService, private oidcConfigService: OidcConfigService) {
    this.oidcConfigService.onConfigurationLoaded.subscribe((configResult: ConfigResult) => {
      // Use the configResult to set the configurations
      const config: OpenIdConfiguration = {
        stsServer: configResult.customConfig.stsServer,
        redirect_url: configResult.customConfig.redirect_url,
        // The Client MUST validate that the aud (audience) Claim contains its client_id value registered at the Issuer
        // identified by the iss (issuer) Claim as an audience.
        // The ID Token MUST be rejected if the ID Token does not list the Client as a valid audience,
        // or if it contains additional audiences not trusted by the Client.
        client_id: configResult.customConfig.client_id,
        response_type: configResult.customConfig.response_type,
        scope: configResult.customConfig.scope,
        post_logout_redirect_uri: configResult.customConfig.post_logout_redirect_uri,
        start_checksession: configResult.customConfig.start_checksession,
        silent_renew: configResult.customConfig.silent_renew,
        silent_renew_url: configResult.customConfig.silent_renew_url,
        post_login_route: configResult.customConfig.startup_route,
        // HTTP 403
        forbidden_route: configResult.customConfig.forbidden_route,
        // HTTP 401
        unauthorized_route: configResult.customConfig.unauthorized_route,
        log_console_warning_active: configResult.customConfig.log_console_warning_active,
        log_console_debug_active: configResult.customConfig.log_console_debug_active,
        // id_token C8: The iat Claim can be used to reject tokens that were issued too far away from the current time,
        // limiting the amount of time that nonces need to be stored to prevent attacks.The acceptable range is Client specific.
        max_id_token_iat_offset_allowed_in_seconds: configResult.customConfig.max_id_token_iat_offset_allowed_in_seconds,
        auto_userinfo: configResult.customConfig.auto_userinfo,
        // all other properties you want to set
      };

      this.oidcSecurityService.setupModule(config, configResult.authWellknownEndpoints);
      //
      this.oidcSecurityService.setCustomRequestParameters({ pres_req_conf_id: configResult.customConfig.pres_req_conf_id });
    });
  }
}
