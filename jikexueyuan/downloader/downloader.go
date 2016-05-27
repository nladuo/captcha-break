package main

import (
	"crypto/md5"
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"os"
	// "time"
)

func getMd5String(s string) string {
	h := md5.New()
	h.Write([]byte(s))
	return hex.EncodeToString(h.Sum(nil))

}

func getGuid() string {
	b := make([]byte, 48)

	if _, err := io.ReadFull(rand.Reader, b); err != nil {
		return ""
	}
	return getMd5String(base64.URLEncoding.EncodeToString(b))
}

func main() {
	for i := 0; i < 500; i++ {
		resp, err := http.Get("http://passport.jikexueyuan.com/sso/verify?1463850163692")
		if err != nil {
			continue
		}
		fmt.Println(resp.ContentLength)
		filename := "./captchas/" + getGuid() + ".gif"
		file, err := os.Create(filename)
		if err != nil {
			continue
		}
		io.Copy(file, resp.Body)
		resp.Body.Close()
		fmt.Println(filename)
	}

}
