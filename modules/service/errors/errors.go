/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	er "memar/error"
	"memar/protocol"
)

const domainEnglish = "Achaemenid"
const domainPersian = "فرمانده"

// Services Errors
var (
	ErrSDKNotFound = New("domain/error.protocol; type=error; name=sdk-not-found")
	.SetDetail(protocol.LanguageEnglish, domainEnglish, "SDK Not Found",
		"Requested software errors SDK in desire human language not found",
		"Contact administrator of software and ask add needed data",
		"You can use online translator and desire human language to errors details")
	.SetDetail(protocol.LanguagePersian, domainPersian, "بسته توسعه یافت نشد",
			"بسته توسعه نرم افزار برای خطاهای این نرم افزار برای زبان انسانی مورد نظر شما یافت نشد",
			"برای بدست آوردن داده های مورد نظر خود با پشتیبان نرم افزار تماس حاصل فرمایید",
			"شما می توانید با استفاده از سرویس های ترجمه آنلاین اطلاعات مورد نیاز ارورها را در زبان انسانی مورد نظر اضافه کنید")

	ErrNotStandardStructureID.Init("domain/mediatype.protocol; type=error; name=not-standard-structure-id")
	.SetDetail(protocol.LanguageEnglish, domainEnglish, "Not Standard StructureID",
		"Given structure to register set non standard ID, It can cause some bad situation in your platform",
		"",
		"")

	ErrFileNameIsNotValid.Init("domain/achaemenid.protocol; type=error; name=file-name-is-not-valid").
				SetDetail(protocol.LanguageEnglish, domainEnglish, "File Name Is Not Valid",
			"Requested file name is not exist or in bad shape",
			"",
			"")
)

// Services Errors
var (
	ErrServiceNameIsNotValid.Init("domain/achaemenid.protocol; type=error; name=service-name-is-not-valid")
	.SetDetail(protocol.LanguageEnglish, domainEnglish, "Service Name Is Not Valid",
			"Requested service name is not exist or in bad shape",
			"",
			"")
)
