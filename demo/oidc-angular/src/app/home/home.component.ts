import {Component, OnDestroy, OnInit} from '@angular/core';
import {OidcSecurityService, TokenHelperService} from 'angular-auth-oidc-client';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  isAuthenticated: boolean;
  isAuthorizedSubscription: Subscription;
  userDataSubscription: Subscription;
  userData: any;

  constructor(
    // private oauthService: OAuthService,
    public oidcSecurityService: OidcSecurityService,
    public tokenHelperService: TokenHelperService) {
    this.isAuthenticated = false;

    if (this.oidcSecurityService.moduleSetup) {
      this.doCallbackLogicIfRequired();
    } else {
      this.oidcSecurityService.onModuleSetup.subscribe(() => {
        this.doCallbackLogicIfRequired();
      });
    }
  }

  private doCallbackLogicIfRequired() {
    // Will do a callback, if the url has a code and state parameter.
    this.oidcSecurityService.authorizedCallbackWithCode(window.location.toString());
  }

  ngOnInit() {
    this.isAuthorizedSubscription = this.oidcSecurityService.getIsAuthorized().subscribe(auth => {
      this.isAuthenticated = auth;
    });
    this.userDataSubscription = this.oidcSecurityService.getUserData().subscribe( data => {
      this.userData = data;
    });
  }

  ngOnDestroy() {
    this.isAuthorizedSubscription.unsubscribe();
    this.userDataSubscription.unsubscribe();
  }

  login() {
    this.oidcSecurityService.authorize();
  }

  logout() {
    this.oidcSecurityService.logoff();
  }

  get id_token() {
    return this.oidcSecurityService.getIdToken();
  }

  get token() {
    return this.oidcSecurityService.getToken();
  }

  get roles() {
    const payload = this.tokenHelperService.getPayloadFromToken(this.oidcSecurityService.getToken(), false);
    const roles: string[] = payload.realm_access.roles;
    return roles;
  }

  get accessTokenPayload() {
    return this.tokenHelperService.getPayloadFromToken(this.oidcSecurityService.getToken(), false);
  }
}
