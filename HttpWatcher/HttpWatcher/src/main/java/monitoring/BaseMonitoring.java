/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package monitoring;

import org.littleshoot.proxy.DefaultHttpProxyServer;
import org.littleshoot.proxy.HttpFiltersAdapter;
import org.littleshoot.proxy.HttpFiltersSourceAdapter;
import io.netty.handler.codec.http.HttpRequest;
import io.netty.handler.codec.http.HttpResponse;
import io.netty.handler.codec.http.HttpObject;
public class BaseMonitoring {
    
    
    public static void ProxyStart(){
        DefaultHttpProxyServer.bootstrap()
            .withPort(8080)
            .withFiltersSource(new HttpFiltersSourceAdapter() {
                @Override
                public HttpFiltersAdapter filterRequest(HttpRequest originalRequest) {
                    return new HttpFiltersAdapter(originalRequest) {
                        @Override
                        public HttpResponse clientToProxyRequest(HttpObject httpObject) {
                            System.out.println("Request: " + originalRequest.uri());
                            return null;
                        }

                        @Override
                        public HttpObject proxyToClientResponse(HttpObject httpObject) {
                            if (httpObject instanceof HttpResponse) {
                                HttpResponse response = (HttpResponse) httpObject;
                                System.out.println("Response: " + response.status());
                            }
                            return httpObject;
                        }
                    };
                }
            })
            .start();
    }
    
}
