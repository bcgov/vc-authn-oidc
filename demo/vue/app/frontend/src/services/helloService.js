import { appAxios } from '@/services/interceptors';
import { ApiRoutes } from '@/utils/constants';

export default {
  /**
   * @function getHello
   * Fetch the contents of the hello endpoint
   * @returns {Promise} An axios response
   */
  getHello() {
    return appAxios().get(ApiRoutes.HELLO);
  }
};
