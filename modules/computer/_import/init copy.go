/* For license and copyright information please see the LEGAL file in the code repository */
// Auto-generated, edits will be overwritten

package modules

/*
import (
	"libgo/achaemenid"
	"libgo/log"
	"libgo/protocol"

	qd "org/modules/quiddity-domain"
)

var (
	adminUserID = [32]byte{128}
	adminOrgID  = [32]byte{192}
)

// Init method use to initialize services and register them in the application.
func Init() {
	qd.RegisterServices()

	// PersonAuthentication
	protocol.App.RegisterService(&registerPersonService)
	protocol.App.RegisterService(&changePersonPasswordService)
	protocol.App.RegisterService(&blockPersonService)
	protocol.App.RegisterService(&recoverPersonAccountService)
	protocol.App.RegisterService(&revokePersonPublicKeyService)
	protocol.App.RegisterService(&unblockPersonService)
	protocol.App.RegisterService(&getPersonStatusService)

	// PersonNumber
	protocol.App.RegisterService(&registerPersonNumberService)
	protocol.App.RegisterService(&getPersonNumberStatusService)
	protocol.App.RegisterService(&getPersonNumberService)
	// protocol.App.RegisterService(&)

	// UserAppConnection
	protocol.App.RegisterService(&authenticateAppConnectionService)
	protocol.App.RegisterService(&findUserAppConnectionService)
	protocol.App.RegisterService(&getUserAppConnectionService)
	protocol.App.RegisterService(&findUserAppConnectionByGivenDelegateService)
	protocol.App.RegisterService(&findUserAppConnectionByGottenDelegateService)
	protocol.App.RegisterService(&registerUserAppConnectionService)
	protocol.App.RegisterService(&updateUserAppConnectionService)
	// protocol.App.RegisterService(&)

	// PersonPublicKey
	protocol.App.RegisterService(&approvePersonPublicKeyService)
	protocol.App.RegisterService(&authenticatePersonPublicKeyService)

	// OrganizationAuthentication
	protocol.App.RegisterService(&registerNewOrganizationService)
	protocol.App.RegisterService(&updateOrganizationService)
	protocol.App.RegisterService(&getOrganizationService)
	protocol.App.RegisterService(&getLastOrganizationsIDService)
	// protocol.App.RegisterService(&blockOrgService)
	// protocol.App.RegisterService(&)

	// ProductAuction
	protocol.App.RegisterService(&registerDefaultProductAuctionService)
	protocol.App.RegisterService(&registerCustomProductAuctionService)
	protocol.App.RegisterService(&updateProductAuctionService)
	protocol.App.RegisterService(&getProductAuctionService)
	protocol.App.RegisterService(&findProductAuctionByDistributionCenterIDService)
	protocol.App.RegisterService(&findProductAuctionByGroupIDService)
	protocol.App.RegisterService(&findProductAuctionByOrgIDService)
	protocol.App.RegisterService(&findProductAuctionByQuiddityIDDistributionCenterIDService)
	protocol.App.RegisterService(&findProductAuctionByQuiddityIDGroupIDService)
	protocol.App.RegisterService(&findProductAuctionByQuiddityIDService)

	// ProductPrice
	protocol.App.RegisterService(&registerProductPriceService)
	protocol.App.RegisterService(&updateProductPriceService)
	protocol.App.RegisterService(&getProductPriceService)
	protocol.App.RegisterService(&findProductPriceByOrgIDService)
	// protocol.App.RegisterService(&)

	// Product
	protocol.App.RegisterService(&registerProductInventoryService)
	// protocol.App.RegisterService(&approveProductAuctionByWarehouseService)
	protocol.App.RegisterService(&getProductService)
	protocol.App.RegisterService(&findProductByQuiddityIDDcIDService)
	protocol.App.RegisterService(&findProductByQuiddityIDOwnerIDService)
	protocol.App.RegisterService(&findProductQuidditiesIDByDCIDService)
	protocol.App.RegisterService(&getProductInventoryDCQuiddityNumberService)
	// protocol.App.RegisterService(&)
	protocol.App.RegisterService(&registerProductInvoiceService)

	// FinancialTransaction
	protocol.App.RegisterService(&registerFinancialTransactionService)
	protocol.App.RegisterService(&getFinancialTransactionService)
	protocol.App.RegisterService(&findFinancialTransactionByDayService)

	// ForeignDetail
	// protocol.App.RegisterService(&)
	// protocol.App.RegisterService(&)
	// protocol.App.RegisterService(&)
	// protocol.App.RegisterService(&)

	// OrganizationStaff
	// protocol.App.RegisterService(&approveOrgPositionByPersonService)
	// protocol.App.RegisterService(&)
	// protocol.App.RegisterService(&)
	// protocol.App.RegisterService(&)
	// protocol.App.RegisterService(&)

	// Common Services
	protocol.App.RegisterService(&sendOtpService)
	protocol.App.RegisterService(&sendSMStoUsersService)
}
*/
