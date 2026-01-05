/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

// service: reserve seat

// FIND_InvoiceIDs_BY_ProductIDAndSeatID(productID pp.UUID, seatID uint64, offset, limit uint64) (invoiceIDs []invoice_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// FIND_InvoiceIDs_BY_SeatID_AND_Status(seatID uint64, status Status, offset, limit uint64) (invoiceIDs []invoice_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// FILTER_InvoiceIDs_BY_Status(status Status, offset, limit uint64) (invoiceIDs []invoice_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
