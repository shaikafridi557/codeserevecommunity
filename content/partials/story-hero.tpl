            <!-- ========== Story Hero (scroll-driven "film": Chaos → Code → Calm) — assets/css/story.css + assets/js/story.js ========== -->
            <section class="st" id="story" aria-label="The CodeServe story">
                <div class="st-pin">
                    <div class="st-stage">
                        <div class="st-grain" aria-hidden="true"></div>
                        <div class="st-glow" aria-hidden="true"></div>

                        <div class="st-shade" aria-hidden="true"></div>
                        <!-- scene captions -->
                        <p class="st-cap st-cap-1" aria-hidden="true"><span class="st-line"><span>Every business</span></span><span class="st-line"><span>has a <em>story.</em></span></span></p>
                        <p class="st-cap st-cap-2" aria-hidden="true"><span class="st-line"><span>Missed calls. Lost orders.</span></span><span class="st-line"><span><em>Endless spreadsheets.</em></span></span></p>
                        <p class="st-cap st-cap-3" aria-hidden="true"><span class="st-line"><span>Then we write</span></span><span class="st-line"><span>the <em>next chapter.</em></span></span></p>
                        <p class="st-cap st-cap-4" aria-hidden="true"><span class="st-line"><span>Websites. Apps. AI agents.</span></span><span class="st-line"><span><em>One calm system.</em></span></span></p>

                        <!-- scene 2: chaos -->
                        <div class="st-chaos" aria-hidden="true">
                            <div class="st-note st-n-wa" data-t="0"><b>WhatsApp</b><span>"Is this still available??"</span><i>12 unread</i></div>
                            <div class="st-note st-n-call" data-t="1"><b>Missed call (3)</b><span>Unknown number · 10:42 PM</span></div>
                            <div class="st-note st-n-order" data-t="2"><b>Order #212</b><span>"Where is my order?"</span></div>
                            <div class="st-note st-n-xls" data-t="3"><b>sales_FINAL_v7.xlsx</b><span>Last edited 3 weeks ago</span></div>
                            <div class="st-note st-n-sticky" data-t="4"><b>call back Ravi!!</b><span>re: quotation</span></div>
                            <div class="st-note st-n-mail" data-t="5"><b>Inbox (48)</b><span>Invoice overdue · Re: Re: Re:</span></div>
                            <div class="st-note st-n-wa2" data-t="0"><b>WhatsApp</b><span>"Hello? Anyone there?"</span></div>
                            <div class="st-note st-n-cal" data-t="4"><b>Double booked</b><span>Tue 11:00 · 2 customers</span></div>
                        </div>

                        <!-- scene 3: code -->
                        <div class="st-code" aria-hidden="true">
                            <pre><span class="st-l"><i>01</i><b class="k">const</b> business = <b class="f">listen</b>(customers);</span>
<span class="st-l"><i>02</i><b class="k">on</b>(<b class="s">'whatsapp'</b>, msg =&gt; ai.<b class="f">reply</b>(msg));</span>
<span class="st-l"><i>03</i><b class="k">on</b>(<b class="s">'order'</b>, o =&gt; kitchen.<b class="f">notify</b>(o));</span>
<span class="st-l"><i>04</i>bookings.<b class="f">remind</b>({ before: <b class="n">'2h'</b> });</span>
<span class="st-l"><i>05</i>sheets.<b class="f">replaceWith</b>(dashboard);</span>
<span class="st-l"><i>06</i>leads.<b class="f">follow</b>(<b class="k">until</b>: <b class="s">'closed'</b>);</span>
<span class="st-l"><i>07</i>website.<b class="f">rank</b>(<b class="s">'Hyderabad'</b>);</span>
<span class="st-l"><i>08</i><b class="k">return</b> <b class="f">calm</b>();</span></pre>
                        </div>

                        <!-- scenes 4–5: device whose screen is the calm dashboard -->
                        <div class="st-device" aria-hidden="true">
                            <div class="st-laptop">
                                <div class="st-bezel">
                                    <div class="st-screen">
                                        <div class="st-dash">
                                            <div class="st-tile st-t0"><small>Chats answered</small><strong>318</strong><em>replies in 3 sec</em></div>
                                            <div class="st-tile st-t1"><small>Calls missed</small><strong>0</strong><em>AI took them</em></div>
                                            <div class="st-tile st-t2"><small>Orders today</small><strong>128</strong><em>all on track</em></div>
                                            <div class="st-tile st-t3 st-chart"><small>Revenue · this month</small><span class="st-bars"><i style="--h:38%"></i><i style="--h:52%"></i><i style="--h:46%"></i><i style="--h:64%"></i><i style="--h:58%"></i><i style="--h:76%"></i><i style="--h:70%"></i><i style="--h:92%"></i></span></div>
                                            <div class="st-tile st-t4"><small>Follow-ups</small><strong>42</strong><em>sent automatically</em></div>
                                            <div class="st-tile st-t5"><small>Bookings</small><strong>36</strong><em>reminders on</em></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="st-base"></div>
                            </div>
                            <div class="st-phone">
                                <div class="st-phone-in">
                                    <span class="st-bubble st-b-in">Is the table for 4 free tonight?</span>
                                    <span class="st-bubble st-b-out">Yes! 8:30 PM is free. Shall I book it? ✓</span>
                                    <span class="st-bubble st-b-in">Yes please</span>
                                    <span class="st-bubble st-b-out st-b-ok">Booked ✓ See you at 8:30</span>
                                </div>
                            </div>
                        </div>

                        <!-- scene 5: our work flying in -->
                        <div class="st-cards" aria-hidden="true">
                            <img class="st-card st-c1" src="assets/img/portfolio/ai-lead-agent-640.webp" alt="" width="640" height="400" loading="lazy" decoding="async">
                            <img class="st-card st-c2" src="assets/img/portfolio/ordering-app-640.webp" alt="" width="640" height="400" loading="lazy" decoding="async">
                            <img class="st-card st-c3" src="assets/img/portfolio/garishta-infra-640.webp" alt="" width="640" height="400" loading="lazy" decoding="async">
                        </div>

                        <!-- final frame (real content, readable without JS) -->
                        <div class="st-final">
                            <h1 class="st-h1">Website Development &amp; AI Automation Company in Hyderabad</h1>
                            <p class="st-title"><span class="st-line"><span>Built</span></span><span class="st-line"><span><em>different.</em></span></span></p>
                            <p class="st-sub">Websites that bring enquiries, software that saves hours and AI agents that work while you sleep — designed and built in KPHB, Hyderabad.</p>
                            <div class="st-ctas">
                                <a class="st-btn st-btn-main" href="contact.html">Start a project <span aria-hidden="true">↗</span></a>
                                <a class="st-btn" href="portfolio.html">See our work</a>
                            </div>
                        </div>

                        <!-- film UI -->
                        <div class="st-ui" aria-hidden="true">
                            <span class="st-scene">SCENE <b>01</b> / 05</span>
                            <span class="st-rec"><i></i>CODESERVE · HYDERABAD</span>
                        </div>
                        <div class="st-bar" aria-hidden="true"><i class="st-fill"></i><span></span><span></span><span></span><span></span><span></span></div>
                        <div class="st-hint" aria-hidden="true">Scroll to play <span>▶</span></div>
                        <button type="button" class="st-skip">Skip intro ↓</button>
                        <div class="st-letterbox st-lb-top" aria-hidden="true"></div>
                        <div class="st-letterbox st-lb-bot" aria-hidden="true"></div>
                    </div>
                </div>
            </section>
            <!-- ========== End Story Hero ========== -->
