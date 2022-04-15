using HTTP, JSON

function job(req::HTTP.Request)
    d = JSON.parse(String(req.body))
    @info("Julia task running...")
	d["output"] *= 3
	
	return HTTP.Response(200, JSON.json(d))
end


function health(req::HTTP.Request)
    return HTTP.Response(200, JSON.json(Dict("Julia-api"=>"healthy!")))
end

# define REST endpoints to dispatch to "service" functions
const ROUTER = HTTP.Router()

HTTP.@register(ROUTER, "POST", "/job", job)
HTTP.@register(ROUTER, "GET", "/health", health)
HTTP.serve(ROUTER, "0.0.0.0", 8081, reuseaddr=true)
