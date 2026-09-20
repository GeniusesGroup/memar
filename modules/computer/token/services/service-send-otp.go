/* For license and copyright information please see the LEGAL file in the code repository */

package pa

import (
	"golang.org/x/crypto/sha3"
	"strconv"

	"libgo/authorization"
	"libgo/convert"
	er "libgo/error"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	lang "libgo/language"
	"libgo/otp"
	asanak "libgo/SDK/asanak.com/go"
	"libgo/srpc"
	"libgo/syllab"
)

// https://tools.ietf.org/html/rfc6238
var sendOtpService = service.Service{
	URN:                "urn:giti:sabz.city:service:send-otp",
	Domain:             DomainName,
	ID:                 15256540144757302302,
	IssueDate:          1592374531,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_Org,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "SendOtp",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: `Request to get approve code for given phone or email.
It can use for many purpose e.g. to recover person, improve account security by force use OTP in some very dangerous operation`,
	},
	TAGS: []string{
		"Authentication",
	},

	SRPCHandler: SendOtpSRPC,
	ServeHTTP: SendOtpHTTP,
}

// SendOtpSRPC is sRPC handler of SendOtp service.
func SendOtpSRPC(st protocol.Stream) {
	var req = &sendOtpReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *sendOtpRes
	res, err = sendOtp(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// SendOtpHTTP is HTTP handler of SendOtp service.
func SendOtpHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &sendOtpReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *sendOtpRes
	res, err = sendOtp(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

const (
	smsOTPDigits = 8
	smsOTPPeriod = 30 * 60 // 30 minutes

	smsOTPEnglish = "SabzCity\n\nYour OTP\n"
	smsOTPPersian = "شهرسبز\nرمز یکبار مصرف\n\n"
)

type sendOtpReq struct {
	CaptchaID   [16]byte `json:",string"`
	Email       string   `valid:"Email"`
	PhoneNumber uint64   `valid:"PhoneNumber"`
	PhoneType   uint8    // 0:SMS 1:call
	Language    protocol.Language
}

type sendOtpRes struct {
	OTPID uint64
}

func sendOtp(st protocol.Stream, req *sendOtpReq) (res *sendOtpRes, err protocol.Error) {
	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	if st.Connection.UserType == protocol.UserType_Unset {
		// TODO::: Prevent DDos attack by do some easy process for user e.g. captcha is not good way!
		err = phraseCaptchas.Check(req.CaptchaID)
		if err != nil {
			return
		}
	}

	res = &sendOtpRes{}

	if req.Email != "" {
		var otpReq = otp.GenerateTimeOTPReq{
			Hasher:     sha512.New512_256(),
			SecretKey:  smsOTPSecurityKey,
			Additional: convert.UnsafeStringToByteSlice(req.Email),
			Period:     smsOTPPeriod,
			Digits:     smsOTPDigits,
		}
		var timeOTP uint64
		timeOTP, err = otp.GenerateTimeOTP(&otpReq)
		if err != nil {
			return
		}

		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Desire Email OTP:", timeOTP))
		} else {
			// TODO::: send OTP to desire email address
		}
	}

	if req.PhoneNumber > 0 {
		var otpReq = otp.GenerateTimeOTPReq{
			Hasher:     sha512.New512_256(),
			SecretKey:  smsOTPSecurityKey,
			Additional: make([]byte, 8),
			Period:     smsOTPPeriod,
			Digits:     smsOTPDigits,
		}
		syllab.SetUInt64(otpReq.Additional, 0, req.PhoneNumber)
		var timeOTP uint64
		timeOTP, err = otp.GenerateTimeOTP(&otpReq)
		if err != nil {
			return
		}

		// if protocol.AppMode_Dev {
		// 	protocol.App.Log(log.DebugEvent(domainEnglish, "Desire Phone OTP:", timeOTP)
		// } else {
		if req.PhoneType == 0 {
			var SendSMSReq = asanak.SendSMSReq{
				Destination: []string{strconv.FormatUint(req.PhoneNumber, 10)},
			}
			switch req.Language {
			case protocol.LanguagePersian:
				SendSMSReq.Message = make([]byte, 0, len(smsOTPPersian)+smsOTPDigits+len(achaemenid.App.Manifest.DomainName)+smsOTPDigits+5)
				SendSMSReq.Message = append(SendSMSReq.Message, smsOTPPersian...)
			default:
				SendSMSReq.Message = make([]byte, 0, len(smsOTPEnglish)+smsOTPDigits+len(achaemenid.App.Manifest.DomainName)+smsOTPDigits+5)
				SendSMSReq.Message = append(SendSMSReq.Message, smsOTPEnglish...)
			}
			SendSMSReq.Message = strconv.AppendUint(SendSMSReq.Message, timeOTP, 10)
			// Add web-otp
			SendSMSReq.Message = append(SendSMSReq.Message, "\n\n@"+achaemenid.App.Manifest.DomainName+" #"...)
			SendSMSReq.Message = strconv.AppendUint(SendSMSReq.Message, timeOTP, 10)

			var SendSMSRes asanak.SendSMSRes
			SendSMSRes, err = smsProvider.SendSMS(&SendSMSReq)
			if err != nil {
				return
			}
			if len(SendSMSRes) > 0 {
				res.OTPID = SendSMSRes[0]
			}
		}
		// }
	}

	return
}

func (req *sendOtpReq) validator() (err protocol.Error) {
	return
}

/*
	Request Encoders & Decoders
*/

func (req *sendOtpReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.CaptchaID[:], buf[0:])
	req.Email = syllab.UnsafeGetString(buf, 16)
	req.PhoneNumber = syllab.GetUInt64(buf, 24)
	req.PhoneType = syllab.GetUInt8(buf, 32)
	req.Language = protocol.Language(syllab.GetUInt8(buf, 33))
	return
}

func (req *sendOtpReq) LenOfSyllabStack() uint32 {
	return 37
}

func (req *sendOtpReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "CaptchaID":
			err = decoder.DecodeByteArrayAsBase64(req.CaptchaID[:])
		case "Email":
			req.Email, err = decoder.DecodeString()
		case "PhoneNumber":
			req.PhoneNumber, err = decoder.DecodeUInt64()
		case "PhoneType":
			req.PhoneType, err = decoder.DecodeUInt8()
		case "Language":
			var num uint32
			num, err = decoder.DecodeUInt32()
			req.Language = protocol.Language(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

/*
	Response Encoders & Decoders
*/

func (res *sendOtpRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetUInt64(buf, 0, res.OTPID)
}

func (res *sendOtpRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *sendOtpRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *sendOtpRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *sendOtpRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"OTPID":`)
	encoder.EncodeUInt64(uint64(res.OTPID))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (res *sendOtpRes) LenAsJSON() (ln int) {
	ln = 30
	return
}
