/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"strings"

)

// ReqDiscountItems is the request structure of "DiscountItems()".
type ReqDiscountItems struct {
	OrganizationID string             `valid:"organizationID"`
	InvoiceID      string             `valid:"invoiceID"`
	Items          map[string]float32 // ManualDiscount e.g. 2.5%
}

// DiscountItems :
// PUT apis.sabz.city/invoices/v1/invoice/{Invoice-UUID}
func DiscountItems(st *achaemenid.Stream, req *ReqDiscountItems) {
	// Check request data.
	logicResponse.Error = validation.ValidateObject(logicRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}
	if !strings.HasPrefix(logicRequest.InvoiceID, logicRequest.OrganizationID) {
		logicResponse.Error = errors.AccessForbidden
		return &logicResponse
	}

	var invoice Invoice
	// Ready dbRequest for database layer.
	dbRequest := usersdata.Request{
		Keys: []string{"Invoice", logicRequest.InvoiceID},
		Data: &invoice}
	logicResponse.Error = usersdata.GetData(&dbRequest)
	if logicResponse.Error != nil {
		return &logicResponse
	}

	// Just related org can approve their items and set manual discount!

	// Set manual discount
	for item, dis := range logicRequest.Items {
		i, ok := invoice.Items[item]
		if !ok {
			logicResponse.Error = errors.InvoiceNotChanged
			return &logicResponse
		}
		i.ManualDiscount = dis
	}

	// We must tell related warehouse about approval to continue process.

	// Write data to Database
	logicResponse.Error = usersdata.UpdateData(&dbRequest)

	return &logicResponse
}
