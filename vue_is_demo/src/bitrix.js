//import { waitBX24 } from './helpers';

export const inIframe =
  window.location !== window.parent.location;

export const inSameDomainIframe = (() => {
  if (!inIframe) { return false; }
  try {
    const parentDocument = window.parent.document;
    return Boolean(parentDocument);
  } catch (_) {
    return false;
  }
})();

export const wait = (f, n) =>
  new Promise(resolve => setTimeout(() => resolve(f()), n));

export const waitBX24 = () => {
  return wait(() => {
    const BX24 = inSameDomainIframe
      ? window.BX24 || window.parent.BX24
      : window.BX24;
    if (!BX24) { return waitBX24(); }
    return BX24;
  }, 50);
};
export class BitrixError extends Error {
  constructor(message) {
    super(message);
    this.name = 'BitrixError';
  }
}
BitrixError.prototype.name = 'BitrixError';

/** РѕР±РµСЂС‚РєР° РЅР°Рґ BX24.callMethod
 * @param {!string} method
 * @param {Object} [data={}]
 * @param {Object} [BX24=window.BX24]
 * @return {!Promise<*>}
 */
export const bxCall = (method, data = {}, BX24 = null) =>
  (BX24 ? Promise.resolve(BX24) : waitBX24())
    .then(BX24 => new Promise((resolve, reject) =>
      BX24.callMethod(method, data, res =>
        // Р’ РґРѕРєР°С… Р·Р°СЏРІР»РµРЅ boolean|string, РЅР° РїСЂР°РєС‚РёРєРµ РІСЃС‚СЂРµС‡Р°РµС‚СЃСЏ undefined
        res.error()
          ? reject(new BitrixError(res.error()))
          : resolve(res.data())
      )
    ));

export const bxCallList = (method, data = {}, BX24 = null) => {
  const result = [];
  return (BX24 ? Promise.resolve(BX24) : waitBX24())
    .then(BX24 => new Promise((resolve, reject) =>
      BX24.callMethod(method, data, res => {
        if (res.error()) { return reject(res.error()); }

        const data = res.data();
        if (!Array.isArray(data)) { return resolve(data); }

        result.push(...data);
        if (res.more()) {
          res.next();
        } else {
          resolve(result);
        }
      })
    ));
};
