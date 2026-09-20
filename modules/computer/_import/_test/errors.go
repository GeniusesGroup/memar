/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	er "../../libgo/error"
	"github.com/GeniusesGroup/libgo/protocol"
)

const domainEnglish = "Sabz.City"
const domainPersian = "شهرسبز"

// Errors
var (
	// Common
	ErrNotImplemented = er.New("urn:giti:sabz.city:error:not-implemented").SetDetail(protocol.LanguageEnglish, domainEnglish, "Not Implemented",
		"Requested service or part of it registered but not implemented yet. Please try agin later.",
		"",
		"").Save()

	ErrBadSituation = er.New("urn:giti:sabz.city:error:bad-situation").SetDetail(protocol.LanguageEnglish, domainEnglish, "Bad Situation",
		"Platform occur bad situation! Developers know about this error and fix it as soon as possible. Please try agin later.",
		"",
		"").Save()

	ErrBlockedByJustice = er.New("urn:giti:sabz.city:error:blocked-by-justice").SetDetail(protocol.LanguageEnglish, domainEnglish, "Blocked By Justice",
		"Given request to register||update||delete a data on a record that blocked by justice department for some reason",
		"",
		"").Save()

	// Quiddity
	ErrQuiddityTitleRegistered = er.New("urn:giti:sabz.city:error:quiddity-title-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Quiddity Title Registered",
		"Given quiddity title to register already registered and active for other one!",
		"",
		"").Save()

	ErrQuiddityURIRegistered = er.New("urn:giti:sabz.city:error:quiddity-uri-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Quiddity URI Registered",
		"Given quiddity URI to register already registered and active for other one!",
		"",
		"").Save()

	// ProductAuction
	ErrProductAuctionRegistered = er.New("urn:giti:sabz.city:error:product-auction-registerd").SetDetail(protocol.LanguageEnglish, domainEnglish, "Product Auction Registered",
		"Product auction already registered and active! Please edit it for any changes",
		"",
		"").Save()

	ErrProductAuctionDefaultNotRegistered = er.New("urn:giti:sabz.city:error:product-auction-default-not-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Product Auction Default Not Registered",
		"Default product auction not register yet! So you can't register custom auction!",
		"",
		"").Save()

	ErrProductAuctionNotRegistered = er.New("urn:giti:sabz.city:error:product-auction-not-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Product Auction Not Registered",
		"Desire product auction not register yet! So you can't update it!",
		"",
		"").Save()

	// ProductPrice
	ErrProductPriceNotRegistered = er.New("urn:giti:sabz.city:error:product-price-not-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Product Price Not Registered",
		"Product price not register yet! So you can't update it!",
		"",
		"").Save()

	// Product Invoice
	ErrProductInvoiceDelegate = er.New("urn:giti:sabz.city:error:product-invoice-delegate").SetDetail(protocol.LanguageEnglish, domainEnglish, "Invoice - Register Delegate",
		"User of the connection can't register delegate invoice without send valid OTP or Transaction ID of desire user",
		"",
		"").
		SetDetail(protocol.LanguagePersian, domainPersian, "فاکتور - ثبت وکالتی",
			"ثبت فاکتور وکالتی بدون ارسال رمز یکبار مصرف یا شماره پرداختی معتبر کاربر مورد نظر امکان پذیر نمی باشد",
			"",
			"").Save()
	ErrProductInvoiceDelegateBadTransactionID = er.New("urn:giti:sabz.city:error:product-invoice-delegate-bad-transaction-id").SetDetail(protocol.LanguageEnglish, domainEnglish, "Invoice - Bad Transaction ID",
		"User of the connection can't register delegate invoice without send valid Transaction ID of desire user with exactly same amount",
		"",
		"").
		SetDetail(protocol.LanguagePersian, domainPersian, "فاکتور - شماره پرداختی نامعتبر",
			"ثبت وکالتی فاکتور برای خریدار مدنظر بدلیل عدم ارسال شماره پرداختی معتبر یا عدم تطابق مبلغ پرداختی با فاکتور امکان پذیر نمی باشد",
			"",
			"").Save()
	ErrProductInvoiceBadDC = er.New("urn:giti:sabz.city:error:product-invoice-bad-dc").SetDetail(protocol.LanguageEnglish, domainEnglish, "Invoice - Bad Request",
		"Desire request to register invoice is not valid and Distributed-Center ID is missing or bad",
		"",
		"").
		SetDetail(protocol.LanguagePersian, domainPersian, "فاکتور - درخواست بد",
			"درخواست جهت ثبت فاکتور بدلیل عدم ارسال یا ارسال مرکز پخش نامعتبر امکان پذیر نمی باشد",
			"",
			"").Save()
)
