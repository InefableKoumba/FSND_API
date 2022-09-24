/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-54fyw4qw.us', // the auth0 domain prefix
    audience: 'coffe_shop_api', // the audience set for the auth0 app
    clientId: 'FKRCE5hIBVF0RxyaqQsBT2U5ipcYOyNc', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:4200', // the base url of the running ionic application. 
  }
};
