import React, { useEffect, useState } from "react";
import PageWrapper from "../PageWrapper";
import { ProductData } from "../../components/interfaces";
import { getProducts } from "../ApiHelper";
import Spinner from "../../components/Spinner/Spinner";

const ProductsPage = () => {
  const [loadingState, setLoadingState] = useState(true);
  const [errorMessage, setErrorMessage] = useState(false);
  const [data, setData] = useState({ Products: [] } as ProductData);

  const getProductAPI = async () => {
    const { productData, errorOccured } = await getProducts();
    setLoadingState(false);
    console.log(productData);
    if (errorOccured) setErrorMessage(true);
    else setData(productData);
  };

  useEffect(() => {
    getProductAPI();
  }, []);

  return (
    <PageWrapper>
      <div className="container mx-auto p-4">
        {loadingState ? (
          <div
            className="flex flex-row justify-center w-full pt-4"
            data-testid="loading-spinner-container"
          >
            <Spinner />
          </div>
        ) : errorMessage ? (
          <div
            className="flex flex-row justify-center w-full pt-4 text-3xl font-bold text-white"
            data-testid="error-container"
          >
            An error occured fetching the data!
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {data.Products.map((product) => (
              <div
                className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300"
                key={product.ProductID}
              >
                <img
                  className="w-full h-48 object-cover"
                  src={product.ProductPhotoURL}
                  alt={product.ProductName}
                />
                <div className="p-4">
                  <h2 className="text-xl font-semibold mb-2">
                    {product.ProductName}
                  </h2>
                  <p className="text-gray-600 mb-4">
                    Status: {product.ProductStatus}
                  </p>
                  <p className="text-gray-600 text-sm mb-4">
                    ID: {product.ProductID}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </PageWrapper>
  );
};

export default ProductsPage;
