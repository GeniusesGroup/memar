/* For license and copyright information please see the LEGAL file in the code repository */

package label

// The service initiator the process of rule
// Whenever the service called, related rule will be executed.
// e.g.
// if invoice.ChangeStatus() called
// Initiator

// The service called in the process of rule
// or action service
// e.g.
// then call NotifyUser(UserID, InvoiceID)
// then call UserEarnCoin(UserID, invoice.TotalPayment/1000)
// Called
