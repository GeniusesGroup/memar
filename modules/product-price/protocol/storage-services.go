/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"memar/protocol"

	fcp "org/modules/financial-currency/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, currencyID fcp.FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, currencyID fcp.FinancialCurrencyUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_ProductIDs_BY_CurrencyID_AND_Price_RANGE(currencyID fcp.FinancialCurrencyUUID, minPrice, maxPrice protocol.MoneyAmount, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_CurrencyIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (currencyIDs []fcp.FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
