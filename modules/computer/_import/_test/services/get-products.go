/* For license and copyright information please see the LEGAL file in the code repository */

package services

import "../../libgo/achaemenid"

// ReqGetAllProducts is the request structure of "GetAllProducts()".
type ReqGetAllProducts struct {
	OrganizationID string `valid:"organizationID"`
	Offset         string `valid:"offset"`
	Limit          string `valid:"limit"`
}

// ResGetAllProducts is the response structure of "GetAllProducts()".
type ResGetAllProducts struct {
	ProductsIDs [][16]byte
}

// GetAllProducts :
func GetAllProducts(st *achaemenid.Stream, req *ReqGetAllProducts) {
	var logicResponse microservice.LogicResponse

	//Check request data
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	//Ready dbRequest for database layer
	var productIDs ResGetAllProducts
	dbRequest := usersdata.Request{
		Keys: []string{"Product", logicRequest.OrganizationID},
		Data: &productIDs.ProductsIDs,
		Options: usersdata.Options{
			Offset: logicRequest.Offset,
			Limit:  logicRequest.Limit}}
	logicResponse.Error = usersdata.GetKeys(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	//Content-Range: items 40-65/*

	logicResponse.Payload = productIDs
	return &logicResponse
}

// ReqGetProductInfo is the request structure of "GetProductInfo()".
type ReqGetProductInfo struct {
	OrganizationID string `valid:"organizationID"`
	ProductID      string `valid:"productID"`
}

// ResGetProductInfo is the response structure of "GetProductInfo()".
type ResGetProductInfo struct {
	// Status    Status
	// Details   Details
	// Warehouse Warehouse
	// Financial Financial
	// Sales     Sales
}

// GetProductInfo :
func GetProductInfo(st *achaemenid.Stream, req *ReqGetProductInfo) {
	var logicResponse microservice.LogicResponse

	//Check request data
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	//Ready dbRequest for database layer
	var productDetails Product
	dbRequest := usersdata.Request{
		Keys: []string{"Product", logicRequest.ProductID},
		Data: &productDetails}
	logicResponse.Error = usersdata.GetData(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	logicResponse.LastModified = dbRequest.LastModified
	logicResponse.Payload = ResGetProductInfo{productDetails.Status, productDetails.Details, productDetails.Warehouse, productDetails.Financial, productDetails.Sales}
	return &logicResponse
}

// ReqMakeNewProduct is the request structure of "MakeNewProduct()".
type ReqMakeNewProduct struct {
	OrganizationID string `valid:"organizationID,optional"`
	Details        Details
	Warehouse      struct {
		WarehouseID string `valid:"warehouseID,optional"`
		OwnerStock  uint
	}
	// Financial Financial
	// Sales     Sales
}

// ResMakeNewProduct is the response structure of "MakeNewProduct()".
type ResMakeNewProduct struct {
	ProductID string
}

// MakeNewProduct :
func MakeNewProduct(st *achaemenid.Stream, req *ReqMakeNewProduct) {
	//Check request data
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	productID := logicRequest.OrganizationID + code.TimeUUID(20, code.NanoSecondUUID, code.DefaultSinceYear)
	productInfo := Product{
		Status: Status{
			Active: false,
			Global: 0},
		Details: logicRequest.Details,
		Warehouse: Warehouse{
			WarehouseID: logicRequest.Warehouse.WarehouseID,
			OwnerStock:  logicRequest.Warehouse.OwnerStock},
		Financial: logicRequest.Financial,
		Sales:     logicRequest.Sales}

	//Ready dbRequest for database layer
	dbRequest := usersdata.Request{
		Keys: []string{"Product", productID},
		Data: productInfo}
	logicResponse.Error = usersdata.AddData(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	logicResponse.Payload = ResMakeNewProduct{productID}
	return &logicResponse
}

// ReqChangeProductInfo is the request structure of "ChangeProductInfo()".
type ReqChangeProductInfo struct {
	OrganizationID string `valid:"organizationID"`
	ProductID      string `valid:"productID"`
	// Details        Details
	// Financial      Financial
	// Sales          Sales
}

// ChangeProductInfo :
func ChangeProductInfo(st *achaemenid.Stream, req *ReqChangeProductInfo) {
	var logicResponse microservice.LogicResponse

	//Check request data
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	//Ready dbRequest for database layer
	var productDetails Product
	dbRequest := usersdata.Request{
		Keys: []string{"Product", logicRequest.ProductID},
		Data: &productDetails}
	logicResponse.Error = usersdata.GetData(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	// Change "Status" to 01 (ManagerApprove) when this method change data just after creation
	if productDetails.Status.Global == 0 {
		productDetails.Status.Global = 1
	}

	productDetails.Details = logicRequest.Details
	productDetails.Financial = logicRequest.Financial
	productDetails.Sales = logicRequest.Sales

	//Ready dbRequest for database layer
	dbRequest = usersdata.Request{
		Keys: []string{"Product", logicRequest.ProductID},
		Data: productDetails}
	logicResponse.Error = usersdata.UpdateData(&dbRequest)

	return &logicResponse
}

// ReqDeleteProduct is the request structure of "GetProductInfo()".
type ReqDeleteProduct struct {
	OrganizationID string `valid:"organizationID"`
	ProductID      string `valid:"productID"`
}

// DeleteProduct :
func DeleteProduct(st *achaemenid.Stream, req *ReqDeleteProduct) {
	var logicResponse microservice.LogicResponse

	//Check request data
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	//Ready dbRequest for database layer
	dbRequest := usersdata.Request{
		Keys: []string{"Product", logicRequest.ProductID}}
	logicResponse.Error = usersdata.DeleteData(&dbRequest)

	return &logicResponse
}
