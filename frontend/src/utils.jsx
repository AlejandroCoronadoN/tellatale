/**
 * Gets product information by sending a request to the server.
 *
 * @param {string} product_id - The product ID.
 * @param {number} qty - The quantity of the product.
 * @returns {Promise<Object>} - A promise that resolves to the product information.
 */
export const getProduct = async (product_id, qty=1) => {
    product_id = product_id.toString()
    console.log( typeof(product_id))

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/scan_product`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            product_id:product_id,
            quantity: qty,
          }),
        }
      );
      const data = await response.json();
      console.log(data);
      return data;
    } catch (error) {
      return {
        response:
          "**Sorry for the inconvenience - product** \n" + error,
      };
    }
  };

  /**
   * Gets user information by sending a request to the server.
   *
   * @param {string} user_id - The user ID.
   * @returns {Promise<Object>} - A promise that resolves to the user information.
   */
  export const getUser = async (user_id) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/scan_user`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: user_id }),
        }
      );
      const data = await response.json();
      return data;
    } catch (error) {
      return {
        response:
          "**Sorry for the inconvenience - user** \n" + error,
      };
    }
  };
