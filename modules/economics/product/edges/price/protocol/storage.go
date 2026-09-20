/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	fmp "org/modules/economics/money/protocol"
	pp "org/modules/economics/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(productID pp.UUID, currencyID fcp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(productID pp.UUID, currencyID fcp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_ProductIDs_BY_CurrencyID_AND_Price_RANGE(currencyID fcp.UUID, minPrice, maxPrice fmp.Amount, offset, limit uint64) (productIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	LIST_CurrencyIDs_BY_ProductID(productID pp.UUID, offset, limit uint64) (currencyIDs []fcp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
