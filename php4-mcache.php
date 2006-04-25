<?php
/**
 * The memcache() function is a factory function that returns a newly
 * instantiated Memcache object.
 *
 * If an internal error prevents creation of a new object FALSE will be 
 * returned, however under normal circumstances this should never fail.
 */
$mc = memcache();

/**
 * The add_server() method takes 2 arguments, first the hostname of the server, 
 * and second the port on which it is listening.
 *
 * This method may be called multiple times to add any number of servers.  The extension
 * will then hash keys in order to decide which server should be used for a given key.
 *
 * add_server() returns TRUE on success, and FALSE on failure.  Because an actual 
 * connection is not immediately attempted, this should always return TRUE except
 * in the event of an internal error.
 */
$mc->add_server('localhost', '11211');
$mc->add_server('localhost', '11212');

/**
 * Another option to the above memcache() and add_server() calls is to use a persistent
 * memcache object.  This is done by using pmemcache() to initially create the object. 
 * pmemcache() takes 1 or 2 arguments.  The first argument is required and is a string
 * that uniquely identifys the object, any future pmemcache() call with the same string
 * will reuse the persistent object.  The second value is an optional number of seconds,
 * if the number is > 0 then it will be an expiration on the persistent object.
 *
 * Expirations, are useful in scenarios where you have memcache servers sometimes dying. 
 * Imagine that you have 3 servers, and one goes down.  You want to use a persistent connection
 * because otherwise each new page is going to result in waiting for a connection timeout,
 * but at the same time sooner or later you want to retry to see if the server is back up.
 * As such, say you decide you want to retry every 5 minutes, set the expiration passed to
 * pmemcache() to 300, and then the object and the 3 server connections will be cached and 
 * reused for 300 seconds, but after that destroyed and recreated, and as such you will retry
 * the server.
 */
$mc = pmemcache('my_unique_mc_object', 300); // keep it persistent for 5 minutes

/**
 * After creating a persistent object, you may or may not need to add servers.  You only
 * want to add them if the object is newly created, and has not yet been initialized, check
 * as follows.
 */
 if(!$mc->is_initialized()) {
        $mc->add_server('localhost', '11211');
        $mc->add_server('localhost', '11212');

        /**
         * Now that you are done initializing mark the object as initialized so that on
         * the next page load you don't repeat the server adds.
         */
        $mc->set_initialized(TRUE);
 }


$fruit_colors = Array('apple'=>'red', 'orange'=>'orange', 'lemon'=>yellow);

/**
 * The set() method takes 2-3 arguments, the first argument is the key and is required,
 * the second is the value associated with the key and is also required.  
 * 
 * The fourth is an expiration value  to pass to the server.  This defaults to 0 when unset.  
 * A 0 expiration means the data never expires.
 *
 * add() and replace() methods are also provided, these take the same arguments, the only
 * difference in functionality is that an add() call will only succeed if the item is not already
 * in the cache, and a replace() call will only succeed if the item is already in the cache.  
 * set() always succeeds assuming a memcache server was reachable.
 *
 * add(), set(), and replace() all return TRUE on successful addition to the cache, and FALSE on 
 * failure.
 */
$mc->set('fruit_colors', $fruit_colors);

/**
 * The get() method takes either a single string as an argument (the key to retrieve),
 * or an array of strings (multiple keys to retrieve).
 *
 * If a single string was passed, then the function returns the value found in the cache,
 * or FALSE for a cache miss.  If FALSE is the value stored in the cache, then it is 
 * indistinguishable, from a miss, if you need to store FALSE in the cache, then you should
 * pass an Array() with just one string in it to get() in order to trigger the 
 * behavior listed below.
 *
 * When the passed argument was an array, the return value will be an array as well.  
 * This array will contain an entry for each key that was successfully found in the cache.
 * If a miss occurs, then there will simply be no entry in the array for the key. So imagine
 * you call ->get(Array('key1', 'key2', 'key3')); If key1 and key3 are found, but key2 is a 
 * miss the return value is Array('key1'=>'key1 value', 'key3'=>'key3 value'); 
 */
$fruit_colors = $mc->get('fruit_colors');
if($fruit_colors) {
        echo 'Found fruit colors in cache!';
} else {
        echo 'Cache miss for fruit colors!';
}

$request = Array('fruit_colors', 'fruit_prices');
$results = $mc->get($request);

if(isset($results['fruit_colors'])) {
        $fruit_colors = $results['fruit_colors'];
} else {
        //get fruit colors from other source
}

if(isset($results['fruit_prices'])) {
        $fruit_prices = $results['fruit_prices'];
} else {
        //get fruit prices from other source
}

/**
 * The delete() method takes 1 or 2 arguments, the first argument is required
 * and is the key to delete.  The second is a 'hold time' that tells the cache
 * not to allow the key to be set again for a certain number of seconds.  By 
 * default there is no hold time.
 *
 * The method returns TRUE when a key is successfully deleted, or FALSE when it is not.
 */
$mc->delete('fruit_colors');

/**
 * The flush_all() method deletes all keys from all active servers. It takes no
 * arguments.
 *
 * The method returns TRUE except in the case of an internal error preventing
 * successful flushing, it then returns FALSE.
 */
$mc->flush_all();

/**
 * The stats() method takes no arguments and returns an associative
 * array with various statistics related to the cache.
 */
$stats = $mc->stats();
var_dump($stats);

?>
