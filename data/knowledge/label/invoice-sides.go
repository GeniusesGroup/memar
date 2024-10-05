/* For license and copyright information please see the LEGAL file in the code repository */

package label

const (
	InvoiceUsers_Unset = iota
	InvoiceUsers_Seller
	InvoiceUsers_Applicant
	InvoiceUsers_Approver
	InvoiceUsers_Payer
	InvoiceUsers_Consumer
	InvoiceUsers_Customer
	InvoiceUsers_Agent
	InvoiceUsers_Franchise

	// OrdererID that is creator of the invoice e.g. restaurant, drug prescription, sales agent,
	InvoiceUsers_Orderer

	InvoiceUsers_Staff
)
